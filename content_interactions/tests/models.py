# coding=utf-8
from django.db import models
from social_graph import crud_aware
from content_interactions.mixins import LikableMixin, DenounceTargetMixin, FavoriteListItemMixin, RateableMixin


@crud_aware
class A(LikableMixin, DenounceTargetMixin, FavoriteListItemMixin, RateableMixin, models.Model):
    name = models.CharField(max_length=255)
