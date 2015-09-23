# coding=utf-8
from django.db.models.signals import pre_save
from django.db import models
from django.utils.translation import ugettext_lazy as _
from social_graph import object_visited
from content_interactions.signals import (
    item_liked,
    item_disliked,
    item_rated,
    item_rate_modified,
    item_marked_as_favorite,
    item_unmarked_as_favorite,
    item_shared,
    item_denounced,
    item_denounce_removed,
    item_commented,
    item_comment_removed
)
from handlers import (
    like_handler,
    dislike_handler,
    new_rating_handler,
    updated_rating_handler,
    update_cached_rating,
    favorite_mark_handler,
    favorite_unmark_handler,
    share_handler,
    denounce_handler,
    denounce_remove_handler,
    comment_handler,
    comment_deleted_handler,
    visit_handler
)


class BaseProcessor(object):
    fields = None
    pre_save_handlers = None
    handlers = None

    def __init__(self, stats_clazz):
        super(BaseProcessor, self).__init__()
        for name, field in self.get_fields():
            field.contribute_to_class(stats_clazz, name)
        pre_save_handlers = self.get_pre_save_handlers()
        if pre_save_handlers:
            for handler_code, pre_save_handler in pre_save_handlers:
                pre_save.connect(pre_save_handler, sender=stats_clazz, dispatch_uid='%s' % handler_code)
        handlers = self.get_handlers()
        if handlers:
            for handler_code, signal, handler in handlers:
                signal.connect(handler, dispatch_uid='%s_process' % handler_code)
        self.stats_clazz = stats_clazz

    def get_fields(self):
        assert self.fields, "No fields defined for this stats processor."
        return self.fields

    def get_pre_save_handlers(self):
        return self.pre_save_handlers

    def get_handlers(self):
        return self.handlers


class Likes(BaseProcessor):
    fields = (
        ('likes', models.IntegerField(default=0, verbose_name=_('Likes'))),
    )
    handlers = (
        ('item_liked', item_liked, like_handler),
        ('item_disliked', item_disliked, dislike_handler),
    )


class Ratings(BaseProcessor):
    fields = (
        ('ratings', models.IntegerField(default=0, verbose_name=_('Ratings'))),
        ('rating_5_count', models.IntegerField(default=0, verbose_name=_('Ratings of 5'))),
        ('rating_4_count', models.IntegerField(default=0, verbose_name=_('Ratings of 4'))),
        ('rating_3_count', models.IntegerField(default=0, verbose_name=_('Ratings of 3'))),
        ('rating_2_count', models.IntegerField(default=0, verbose_name=_('Ratings of 2'))),
        ('rating_1_count', models.IntegerField(default=0, verbose_name=_('Ratings of 1'))),
        ('rating', models.DecimalField(default=0, decimal_places=1, max_digits=2, verbose_name=_('Average Rating'))),
    )
    pre_save_handlers = (
        ('update_cached_rating', update_cached_rating),
    )
    handlers = (
        ('item_rated', item_rated, new_rating_handler),
        ('item_rate_modified', item_rate_modified, updated_rating_handler),
    )


class FavoriteMarks(BaseProcessor):
    fields = (
        ('favorite_marks', models.IntegerField(default=0, verbose_name=_('Favorite Marks'))),
    )
    handlers = (
        ('item_marked_favorite', item_marked_as_favorite, favorite_mark_handler),
        ('item_unmarked_favorite', item_unmarked_as_favorite, favorite_unmark_handler),
    )


class Shares(BaseProcessor):
    fields = (
        ('shares', models.IntegerField(default=0, verbose_name=_('Shares'))),
    )
    handlers = (
        ('item_shared', item_shared, share_handler),
    )


class Denounces(BaseProcessor):
    fields = (
        ('denounces', models.IntegerField(default=0, verbose_name=_('Denounces'))),
    )
    handlers = (
        ('item_denounced', item_denounced, denounce_handler),
        ('item_denounce_removed', item_denounce_removed, denounce_remove_handler),
    )


class Comments(BaseProcessor):
    fields = (
        ('comments', models.IntegerField(default=0, verbose_name=_('comments'))),
    )
    handlers = (
        ('item_commented', item_commented, comment_handler),
        ('item_comment_removed', item_comment_removed, comment_deleted_handler),
    )


class Visits(BaseProcessor):
    fields = (
        ('visits', models.IntegerField(default=0, verbose_name=_('Visits'))),
    )
    handlers = (
        ('item_visited', object_visited, visit_handler),
    )