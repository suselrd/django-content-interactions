# coding=utf-8
from django.dispatch import Signal

item_liked = Signal(providing_args=['instance', 'user'])
item_disliked = Signal(providing_args=['instance', 'user'])
item_marked_as_favorite = Signal(providing_args=['instance', 'user'])
item_unmarked_as_favorite = Signal(providing_args=['instance', 'user'])
item_rated = Signal(providing_args=['instance', 'user', 'rating'])
item_rate_modified = Signal(providing_args=['instance', 'user', 'old_rating', 'rating'])
item_denounced = Signal(providing_args=['instance', 'user', 'comment'])
item_denounce_removed = Signal(providing_args=['instance', 'user'])

item_shared = Signal(providing_args=['instance', 'user', 'addressee_list'])
item_recommended = Signal(providing_args=['instance', 'user', 'addressee_list', 'comment'])
