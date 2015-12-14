# coding=utf-8
from django.db import models
from social_graph import crud_aware
from content_interactions.mixins import LikableMixin, DenounceTargetMixin, FavoriteListItemMixin, RateableMixin
from content_interactions_monitoring.mixins import MonitoringMixin


@crud_aware
class A(MonitoringMixin, LikableMixin, DenounceTargetMixin, FavoriteListItemMixin, RateableMixin, models.Model):
    name = models.CharField(max_length=255)
