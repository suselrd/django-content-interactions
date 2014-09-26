# coding=utf-8
from django import template
from ..mixins import LikableMixin, FavoriteListItemMixin, RateableMixin
from ..utils import intmin as intmin_function

register = template.Library()


@register.filter
def liked_by(obj, user):
    """
    Returns whether an obj is liked by the passed user or not.
    """
    if user.is_anonymous():
        return False
    if not obj:
        return False
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
    if not isinstance(obj, RateableMixin):
        raise Exception("RateableMixin instance expected")
    return obj.rating(user)



@register.filter(is_safe=False)
def intmin(value):
    """
    """
    return intmin_function(value)