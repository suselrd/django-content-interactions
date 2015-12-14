# coding=utf-8
from django.db.models import Model
from django.contrib.contenttypes import generic
from models import Stats


class StatsMixin(Model):
    stats = generic.GenericRelation(Stats, object_id_field='object_pk', content_type_field='content_type')

    class Meta(object):
        abstract = True
