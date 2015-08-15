# coding=utf-8
from django.contrib.contenttypes.models import ContentType
from content_interactions.mixins import (
    ContentInteractionMixin, LikableMixin, FavoriteListItemMixin, DenounceTargetMixin, RateableMixin
)
from settings import *


@property
def stats(self):
    from content_interactions_stats.models import Stats
    result, created = Stats.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(self.__class__), object_pk=self.pk
    )
    if not created:
        return result
    if hasattr(result, 'likes') and isinstance(self, LikableMixin):
        result.likes = self.likes
    if hasattr(result, 'favorite_marks') and isinstance(self, FavoriteListItemMixin):
        result.favorite_marks = self.favorite_marks
    if hasattr(result, 'ratings') and isinstance(self, RateableMixin):
        result.ratings = self.ratings
        result.rating_5_count = self.rating_of(5)
        result.rating_4_count = self.rating_of(4)
        result.rating_3_count = self.rating_of(3)
        result.rating_2_count = self.rating_of(2)
        result.rating_1_count = self.rating_of(1)
        result.rating = self.avg_rating
    if hasattr(result, 'denounces') and isinstance(self, DenounceTargetMixin):
        result.denounces = self.denounces
    result.save()
    return result


setattr(ContentInteractionMixin, 'stats', stats)
