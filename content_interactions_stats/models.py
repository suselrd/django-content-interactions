# coding=utf-8
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from decorators import stats_container


@stats_container
class Stats(models.Model):
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('Content Type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.IntegerField(_('Object ID'))
    item = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    class Meta(object):
        verbose_name = _('Item Stats')
        verbose_name_plural = _('Item Stats')
        unique_together = ('content_type', 'object_pk')