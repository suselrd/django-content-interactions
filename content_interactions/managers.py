# coding=utf-8
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.encoding import force_text


class CommentQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(is_removed=False)


class CommentManager(models.Manager):

    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db).active()

    def for_model(self, model):
        """
        QuerySet for all comments for a particular model (either an instance or
        a class).
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_queryset().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_text(model._get_pk_val()))
        return qs


class CommentCurrentSiteManager(CurrentSiteManager):

    def get_queryset(self):
        if not self._CurrentSiteManager__is_validated:
            self._validate_field_name()
        return CommentQuerySet(
            self.model, using=self._db
        ).filter(**{self._CurrentSiteManager__field_name + '__id__exact': settings.SITE_ID}).active()