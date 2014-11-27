# coding=utf-8
from django.contrib.contenttypes.models import ContentType
from django import template
from django.core.exceptions import ObjectDoesNotExist
from ..mixins import LikableMixin, FavoriteListItemMixin, RateableMixin, DenounceTargetMixin
from ..utils import intmin as intmin_function

register = template.Library()


def tuple_to_obj(t):
    try:
        obj = ContentType.objects.get(pk=t[0]).get_object_for_this_type(
            **{'pk': t[1]}
        )
    finally:
        return obj or None


@register.filter
def liked_by(obj, user):
    """
    Returns whether an obj is liked by the passed user or not.
    """
    if user.is_anonymous():
        return False
    if not obj:
        return False
    if isinstance(obj, tuple):
        obj = tuple_to_obj(obj)
    if not isinstance(obj, LikableMixin):
        raise Exception("LikableMixin instance expected")
    return obj.liked_by(user)


@register.filter
def favorite_of(obj, user):
    """
    Returns whether an obj is a favorite of the passed user or not.
    """
    if user.is_anonymous():
        return False
    if not obj:
        return False
    if isinstance(obj, tuple):
        obj = tuple_to_obj(obj)
    if not isinstance(obj, FavoriteListItemMixin):
        raise Exception("FavoriteListItemMixin instance expected")
    return obj.favorite_of(user)


@register.filter
def rating_of(obj, user):
    """
    Returns the rating given by the passed user to the passed obj.
    """
    if user.is_anonymous():
        return False
    if not obj:
        return False
    if isinstance(obj, tuple):
        obj = tuple_to_obj(obj)
    if not isinstance(obj, RateableMixin):
        raise Exception("RateableMixin instance expected")
    return obj.rating(user)


@register.filter
def denounced_by(obj, user):
    """
    Returns whether an obj is denounced by the passed user or not.
    """
    if user.is_anonymous():
        return False
    if not obj:
        return False
    if isinstance(obj, tuple):
        obj = tuple_to_obj(obj)
    if not isinstance(obj, DenounceTargetMixin):
        raise Exception("DenounceTargetMixin instance expected")
    return obj.denounced_by(user)


@register.filter(is_safe=False)
def intmin(value):
    """
    """
    return intmin_function(value)