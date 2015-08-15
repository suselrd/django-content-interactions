# coding=utf-8
from django.db import models
from django.utils.module_loading import import_by_path
from processors import BaseProcessor
from settings import CONTENT_INTERACTIONS_STATS_PROCESSORS


def stats_container(clazz):
    if not issubclass(clazz, models.Model):
        return clazz

    if not hasattr(clazz, 'processors'):
        clazz.processors = list()
        for processor in CONTENT_INTERACTIONS_STATS_PROCESSORS:
            processor_class = import_by_path(processor)
            if not issubclass(processor_class, BaseProcessor):
                continue
            processor = import_by_path(processor)(clazz)
            clazz = processor.stats_clazz
            clazz.processors.append(processor)

    return clazz
