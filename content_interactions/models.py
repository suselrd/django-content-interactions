# coding=utf-8
from django.conf import settings
from django.dispatch import receiver

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.encoding import python_2_unicode_compatible

from social_graph import Graph

from managers import CommentManager, CommentCurrentSiteManager
from mixins import author_edge, target_edge
from signals import item_commented, item_comment_removed

graph = Graph()


class BaseCommentAbstractModel(models.Model):
    """
    An abstract base class that any custom comment models probably should
    subclass.
    """

    # Content-object field
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_(u'content type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_(u'object ID'))
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    # Metadata about the comment
    site = models.ForeignKey(Site)

    class Meta:
        abstract = True

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return urlresolvers.reverse(
            "comments-url-redirect",
            args=(self.content_type_id, self.object_pk)
        )


def validate_level(value):
    if value > settings.COMMENT_MAX_LEVELS:
        raise ValidationError(_('Max comment level exceeded.'))


@python_2_unicode_compatible
class Comment(BaseCommentAbstractModel):
    """
    A user comment about some object.
    """

    # Who posted this comment? If ``user`` is set then it was an authenticated
    # user; otherwise at least user_name should have been set and the comment
    # was posted by a non-authenticated user.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'user'),
                             blank=True, null=True, related_name="%(class)s_comments")
    user_name = models.CharField(_(u"name"), max_length=50, blank=True)
    # Explicit `max_length` to apply both to Django 1.7 and 1.8+.
    user_email = models.EmailField(_(u"email"), max_length=254,
                                   blank=True)
    user_url = models.URLField(_(u"user's URL"), blank=True)

    comment = models.TextField(_(u'comment'), max_length=settings.COMMENT_MAX_LENGTH)

    answer_to = models.ForeignKey(
        'self', verbose_name=_(u'answer to'), related_name='answers', blank=True, null=True
    )

    level = models.IntegerField(_(u'comment level'), blank=True, null=True, validators=[validate_level])

    # Metadata about the comment
    submit_date = models.DateTimeField(_(u'date/time submitted'), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_(u'IP address'), unpack_ipv4=True, blank=True, null=True)
    is_public = models.BooleanField(_(u'is public'), default=True,
                                    help_text=_(u'Uncheck this box to make the comment effectively '
                                                u'disappear from the site.'))
    is_removed = models.BooleanField(_(u'is removed'), default=False,
                                     help_text=_(u'Check this box if the comment is inappropriate. '
                                                 u'A "This comment has been removed" message will '
                                                 u'be displayed instead.'))

    # Manager
    objects = CommentManager()
    on_site = CommentCurrentSiteManager()
    historical = models.Manager()

    class Meta:
        ordering = ('submit_date',)
        permissions = [("can_moderate", "Can moderate comments")]
        verbose_name = _(u'comment')
        verbose_name_plural = _(u'comments')

    def __str__(self):
        return "%s: %s..." % (self.name, self.comment[:50])

    @property
    def user_info(self):
        """
        Get a dictionary that pulls together information about the poster
        safely for both authenticated and non-authenticated comments.

        This dict will have ``name``, ``email``, and ``url`` fields.
        """
        if not hasattr(self, "_user_info"):
            user_info = {
                "name": self.user_name,
                "email": self.user_email,
                "url": self.user_url
            }
            if self.user_id:
                u = self.user
                if u.email:
                    user_info["email"] = u.email

                # If the user has a full name, use that for the user name.
                # However, a given user_name overrides the raw user.username,
                # so only use that if this comment has no associated name.
                if u.get_full_name():
                    user_info["name"] = self.user.get_full_name()
                elif not self.user_name:
                    user_info["name"] = u.get_username()
            self._user_info = user_info
        return self._user_info

    def _get_name(self):
        return self.user_info["name"]

    def _set_name(self, val):
        if self.user_id:
            raise AttributeError(_(u"This comment was posted by an authenticated "
                                   u"user and thus the name is read-only."))
        self.user_name = val

    name = property(_get_name, _set_name, doc="The name of the user who posted this comment")

    def _get_email(self):
        return self.user_info["email"]

    def _set_email(self, val):
        if self.user_id:
            raise AttributeError(_(u"This comment was posted by an authenticated "
                                   u"user and thus the email is read-only."))
        self.user_email = val

    email = property(_get_email, _set_email, doc="The email of the user who posted this comment")

    def _get_url(self):
        return self.userinfo["url"]

    def _set_url(self, val):
        self.user_url = val

    url = property(_get_url, _set_url, doc="The URL given by the user who posted this comment")

    def get_absolute_url(self, anchor_pattern="#c%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    def get_as_text(self):
        """
        Return this comment as plain text.  Useful for emails.
        """
        data = {
            'user': self.user or self.name,
            'date': self.submit_date,
            'comment': self.comment,
            'domain': self.site.domain,
            'url': self.get_absolute_url()
        }
        return _(u'Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % data

    def delete(self, using=None):
        for answer in self.answers.all():
            answer.delete()
        self.is_removed = True
        self.save()


@receiver(models.signals.pre_save, sender=Comment, dispatch_uid="fill_comment_user_data")
def fill_comment_user_data(instance, **kwargs):
    if not instance.user_name or not instance.user_email:
        instance.user_name = instance.user.get_full_name() or instance.user.username
        instance.user_email = instance.user.email
    if not instance.level:
        instance.level = instance.answer_to.level + 1 if instance.answer_to else 1


@receiver(models.signals.post_save, sender=Comment, dispatch_uid="manage_comment_edges")
def create_comment_edges(instance, created, **kwargs):
    if created:
        if instance.user:
            graph.edge(instance.user, instance, author_edge(), instance.site, {})
        graph.edge(instance, instance.content_object, target_edge(), instance.site, {})

        item_commented.send(sender=Comment, instance=instance, user=instance.user, answer_to=instance.answer_to)
    elif instance.is_removed:
        if instance.user:
            graph.no_edge(instance.user, instance, author_edge(), instance.site)
        graph.no_edge(instance, instance.content_object, target_edge(), instance.site)

        item_comment_removed.send(
            sender=Comment, instance=instance, user=instance.content_object.get_comments_manager() or instance.user
        )