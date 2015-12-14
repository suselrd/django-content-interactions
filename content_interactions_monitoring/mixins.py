# coding=utf-8
from django.db.models import Model
from django.contrib.contenttypes import generic
from models import ActivityRecord


class MonitoringMixin(Model):
    activity_records = generic.GenericRelation(
        ActivityRecord, object_id_field='object_pk', content_type_field='content_type'
    )

    class Meta(object):
        abstract = True
