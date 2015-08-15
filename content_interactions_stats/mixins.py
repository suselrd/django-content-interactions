# coding=utf-8
from django.contrib.contenttypes import generic
from models import Stats


class StatsMixin(object):
    stats = generic.GenericRelation(Stats, object_id_field='object_pk', content_type_field='content_type')
