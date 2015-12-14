# coding=utf-8
import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.utils.module_loading import import_by_path
from django.utils.translation import ugettext_lazy as _


class ActivityRecordType(models.Model):
    name = models.CharField(_(u'name'), max_length=255, unique=True)
    expiration = models.IntegerField(_(u'expiration, in seconds'), default=60*5, blank=True)

    def __unicode__(self):
        return u"%s" % self.name


class ActivityRecordQuerySet(models.query.QuerySet):

    def current(self):
        return self.filter(expires__gt=datetime.datetime.now())

    def expired(self):
        return self.filter(expires__lte=datetime.datetime.now())


class ActivityRecordManager(models.Manager):

    def current(self):
        return self.get_queryset().current()

    def expired(self):
        return self.get_queryset().expired()

    def get_queryset(self):
        return ActivityRecordQuerySet(self.model, using=self._db)


class ActivityRecord(models.Model):
    type = models.ForeignKey(ActivityRecordType, verbose_name=_(u'type'), related_name='activity_records')
    time = models.DateTimeField(_(u'time'), auto_now_add=True)
    expires = models.DateTimeField(_(u'expires at'), blank=True, editable=False)

    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_(u'Content Type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.IntegerField(_(u'Object ID'))
    item = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    user = models.ForeignKey(User, null=True, blank=True, related_name='activity_records')

    objects = ActivityRecordManager()

    class Meta(object):
        verbose_name = _(u'Activity Record')
        verbose_name_plural = _(u'Activity Records')
        ordering = ('-time',)

    def __unicode__(self):
        return (self.user.get_full_name() or self.user) if self.user else _(u'Anonymous')

    @property
    def is_expired(self):
        return self.expires <= datetime.datetime.now()

    @property
    def is_current(self):
        return self.expires > datetime.datetime.now()


# noinspection PyUnusedLocal
@receiver(models.signals.pre_save, sender=ActivityRecord, dispatch_uid='activity_record_fill_expiration_time')
def fill_expiration_time(instance, **kwargs):
    if not instance.pk and not instance.expires:
        instance.expires = datetime.datetime.now() + datetime.timedelta(seconds=instance.type.expiration)


def load_processors():
    from settings import CONTENT_INTERACTIONS_MONITORING_PROCESSORS
    from processors import BaseProcessor
    for processor in CONTENT_INTERACTIONS_MONITORING_PROCESSORS:
        processor_class = import_by_path(processor)
        if not issubclass(processor_class, BaseProcessor):
            continue
        processor_class()

load_processors()