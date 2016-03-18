# coding=utf-8
import logging
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib.sites.models import Site
from social_graph import Graph
from . import (
    LIKE, LIKED_BY, RATE, RATED_BY, FAVORITE, FAVORITE_OF, DENOUNCE, DENOUNCED_BY,
    AUTHOR, AUTHORED_BY, TARGET, TARGETED_BY
)
from signals import (
    item_liked,
    item_disliked,
    item_marked_as_favorite,
    item_unmarked_as_favorite,
    item_rated,
    item_rate_modified,
    item_denounced,
    item_denounce_removed
)

logger = logging.getLogger(__name__)

graph = Graph()


def like_edge():
    like = cache.get('LIKE_EDGE_TYPE')
    if like is not None:
        return like
    from social_graph.models import EdgeType
    try:
        like = EdgeType.objects.get(name=LIKE)
        cache.set('LIKE_EDGE_TYPE', like)
        return like
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def liked_by_edge():
    liked_by = cache.get('LIKED_BY_EDGE_TYPE')
    if liked_by is not None:
        return liked_by
    from social_graph.models import EdgeType
    try:
        liked_by = EdgeType.objects.get(name=LIKED_BY)
        cache.set('LIKED_BY_EDGE_TYPE', liked_by)
        return liked_by
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def rate_edge():
    rate = cache.get('RATE_EDGE_TYPE')
    if rate is not None:
        return rate
    from social_graph.models import EdgeType
    try:
        rate = EdgeType.objects.get(name=RATE)
        cache.set('RATE_EDGE_TYPE', rate)
        return rate
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def rated_by_edge():
    rated_by = cache.get('RATED_BY_EDGE_TYPE')
    if rated_by is not None:
        return rated_by
    from social_graph.models import EdgeType
    try:
        rated_by = EdgeType.objects.get(name=RATED_BY)
        cache.set('RATED_BY_EDGE_TYPE', rated_by)
        return rated_by
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def favorite_edge():
    favorite = cache.get('FAVORITE_EDGE_TYPE')
    if favorite is not None:
        return favorite
    from social_graph.models import EdgeType
    try:
        favorite = EdgeType.objects.get(name=FAVORITE)
        cache.set('FAVORITE_EDGE_TYPE', favorite)
        return favorite
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def favorite_of_edge():
    favorite_of = cache.get('FAVORITE_OF_EDGE_TYPE')
    if favorite_of is not None:
        return favorite_of
    from social_graph.models import EdgeType
    try:
        favorite_of = EdgeType.objects.get(name=FAVORITE_OF)
        cache.set('FAVORITE_OF_EDGE_TYPE', favorite_of)
        return favorite_of
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def denounce_edge():
    denounce = cache.get('DENOUNCE_EDGE_TYPE')
    if denounce is not None:
        return denounce
    from social_graph.models import EdgeType
    try:
        denounce = EdgeType.objects.get(name=DENOUNCE)
        cache.set('DENOUNCE_EDGE_TYPE', denounce)
        return denounce
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def denounced_by_edge():
    denounced_by = cache.get('DENOUNCED_BY_EDGE_TYPE')
    if denounced_by is not None:
        return denounced_by
    from social_graph.models import EdgeType
    try:
        denounced_by = EdgeType.objects.get(name=DENOUNCED_BY)
        cache.set('DENOUNCED_BY_EDGE_TYPE', denounced_by)
        return denounced_by
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def author_edge():
    author = cache.get('AUTHOR_EDGE_TYPE')
    if author is not None:
        return author
    from social_graph.models import EdgeType
    try:
        author = EdgeType.objects.get(name=AUTHOR)
        cache.set('AUTHOR_EDGE_TYPE', author)
        return author
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def authored_by_edge():
    authored_by = cache.get('AUTHORED_BY_EDGE_TYPE')
    if authored_by is not None:
        return authored_by
    from social_graph.models import EdgeType
    try:
        authored_by = EdgeType.objects.get(name=AUTHORED_BY)
        cache.set('AUTHORED_BY_EDGE_TYPE', authored_by)
        return authored_by
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def target_edge():
    target = cache.get('TARGET_EDGE_TYPE')
    if target is not None:
        return target
    from social_graph.models import EdgeType
    try:
        target = EdgeType.objects.get(name=TARGET)
        cache.set('TARGET_EDGE_TYPE', target)
        return target
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


def targeted_by_edge():
    targeted_by = cache.get('TARGETED_BY_EDGE_TYPE')
    if targeted_by is not None:
        return targeted_by
    from social_graph.models import EdgeType
    try:
        targeted_by = EdgeType.objects.get(name=TARGETED_BY)
        cache.set('TARGETED_BY_EDGE_TYPE', targeted_by)
        return targeted_by
    except EdgeType.DoesNotExist as e:
        logger.exception(e)


class ContentInteractionMixin(object):

    def get_site(self):
        return getattr(self, 'site', Site.objects.get_current())


class LikableMixin(ContentInteractionMixin):
    @property
    def likes(self):
        return graph.edge_count(self, liked_by_edge(), self.get_site())

    @property
    def liking_users(self):
        return [node for node, attributes, time in graph.edge_range(
            self, liked_by_edge(), 0, self.likes, self.get_site()
        )]

    def liked_by(self, user):
        return graph.edge_get(self, liked_by_edge(), user, self.get_site()) is not None

    def like(self, user):
        _edge = graph.edge(user, self, like_edge(), self.get_site(), {})
        if _edge:
            item_liked.send(sender=self.__class__, instance=self, user=user)
        return _edge

    def unlike(self, user):
        _deleted = graph.no_edge(user, self, like_edge(), self.get_site())
        if _deleted:
            item_disliked.send(sender=self.__class__, instance=self, user=user)
        return _deleted


class FavoriteListItemMixin(ContentInteractionMixin):
    @property
    def favorite_marks(self):
        return graph.edge_count(self, favorite_of_edge(), self.get_site())

    @property
    def favorite_marking_users(self):
        return [node for node, attributes, time in graph.edge_range(
            self, favorite_of_edge(), 0, self.favorite_marks, self.get_site()
        )]

    def favorite_of(self, user):
        return graph.edge_get(self, favorite_of_edge(), user, self.get_site()) is not None

    def mark_as_favorite(self, user):
        _edge = graph.edge(user, self, favorite_edge(), self.get_site(), {})
        if _edge:
            item_marked_as_favorite.send(sender=self.__class__, instance=self, user=user)
        return _edge

    def delete_favorite(self, user):
        _deleted = graph.no_edge(user, self, favorite_edge(), self.get_site())
        if _deleted:
            item_unmarked_as_favorite.send(sender=self.__class__, instance=self, user=user)
        return _deleted


class RateableMixin(ContentInteractionMixin):

    @property
    def ratings(self):
        return graph.edge_count(self, rated_by_edge(), self.get_site())

    @property
    def rating_users(self):
        return [node for node, attributes, time in graph.edge_range(
            self, rated_by_edge(), 0, self.ratings, self.get_site()
        )]

    @property
    def avg_rating(self):
        return (
            5 * self.rating_of(5)
            + 4 * self.rating_of(4)
            + 3 * self.rating_of(3)
            + 2 * self.rating_of(2)
            + self.rating_of(1)
        )/(self.ratings * float(1)) if self.ratings else 0

    def rating_of(self, rating_value):
        from social_graph import ATTRIBUTES_INDEX
        _edges = graph.edge_range(self, rated_by_edge(), 0, self.ratings, self.get_site())
        return len([_edge for _edge in _edges if _edge[ATTRIBUTES_INDEX]['rating'] == rating_value])

    def rating(self, user):
        _edge = graph.edge_get(self, rated_by_edge(), user, self.get_site())
        return _edge.attributes['rating'] if _edge is not None else None

    def full_rating(self, user):
        _edge = graph.edge_get(self, rated_by_edge(), user, self.get_site())
        return (
            _edge.attributes['rating'] if _edge is not None else None,
            _edge.attributes['comment'] if _edge is not None else None
        )

    def rated_by(self, user):
        return graph.edge_get(self, rated_by_edge(), user, self.get_site()) is not None

    def save_rate(self, user, rating, comment=None):
        _edge = graph.edge(user, self, rate_edge(), self.get_site(), {'rating': rating, 'comment': comment})
        if _edge:
            item_rated.send(sender=self.__class__, instance=self, user=user, rating=rating, comment=comment)
        return _edge

    def change_rate(self, user, rating, comment=None):
        old_rating = self.rating(user)
        _edge = graph.edge(user, self, rate_edge(), self.get_site(), {'rating': rating, 'comment': comment})
        if _edge:
            item_rate_modified.send(
                sender=self.__class__,
                instance=self,
                user=user,
                old_rating=old_rating,
                rating=rating,
                comment=comment
            )
        return _edge


class DenounceTargetMixin(ContentInteractionMixin):
    @property
    def denounces(self):
        return graph.edge_count(self, denounced_by_edge(), self.get_site())

    @property
    def denouncing_users(self):
        return [node for node, attributes, time in graph.edge_range(
            self, denounced_by_edge(), 0, self.denounces, self.get_site()
        )]

    def denounced_by(self, user):
        return graph.edge_get(self, denounced_by_edge(), user, self.get_site()) is not None

    def denounce_comment(self, user):
        _edge = graph.edge_get(self, denounced_by_edge(), user, self.get_site())
        return _edge.attributes['comment'] if _edge is not None else None

    def denounce(self, user, comment):
        _edge = graph.edge(user, self, denounce_edge(), self.get_site(), {'comment': comment})
        if _edge:
            item_denounced.send(sender=self.__class__, instance=self, user=user, comment=comment)
        return _edge

    def remove_denounce(self, user):
        _deleted = graph.no_edge(user, self, denounce_edge(), self.get_site())
        if _deleted:
            item_denounce_removed.send(sender=self.__class__, instance=self, user=user)
        return _deleted


class CommentTargetMixin(ContentInteractionMixin):

    def get_comments_manager(self, *args, **kwargs):
        if hasattr(self, 'owner'):
            return (
                self.owner if not callable(self.owner)
                else self.owner(*args, **kwargs)
            )
        elif hasattr(self, 'get_owner'):
            return (
                self.get_owner if not callable(self.get_owner)
                else self.get_owner(*args, **kwargs)
            )
        else:
            return None

    @property
    def comment_list(self):
        from .models import Comment
        return Comment.objects.for_model(self)

    @property
    def comments(self):
        return self.comment_list.count()

    @property
    def commenting_users(self):
        return set([comment.user for comment in self.comment_list if comment.user])

    @property
    def commenting_user_pks(self):
        return set([comment.user.pk for comment in self.comment_list if comment.user])

    def commented_by(self, user):
        from django.contrib.auth.models import User
        return isinstance(user, User) and (user.pk in self.commenting_user_pks)


class ShareToSocialNetworkTargetMixin(ContentInteractionMixin):

    def get_picture(self):
        picture = getattr(self, 'picture', None)
        return picture() if callable(picture) else picture

    def get_url(self):
        url = getattr(self, 'url', "")
        return url() if callable(url) else url


class LikableManagerMixin(object):
    graph = graph

    def liked_by(self, user):
        like = like_edge()
        count = self.graph.edge_count(user, like)
        content_type = ContentType.objects.get_for_model(self.model)
        ids = [
            node.pk for node, attributes, time in self.graph.edge_range(user, like, 0, count)
            if ContentType.objects.get_for_model(node) == content_type
        ]
        return self.get_queryset().filter(pk__in=ids)


class FavoriteListItemManagerMixin(object):
    graph = graph

    def favorites(self, user):
        favorite = favorite_edge()
        count = self.graph.edge_count(user, favorite)
        content_type = ContentType.objects.get_for_model(self.model)
        ids = [
            node.pk for node, attributes, time in self.graph.edge_range(user, favorite, 0, count)
            if ContentType.objects.get_for_model(node) == content_type
        ]
        return self.get_queryset().filter(pk__in=ids)


class DenounceTargetManagerMixin(object):
    graph = graph

    def denounced_by(self, user):
        denounce = denounce_edge()
        count = self.graph.edge_count(user, denounce)
        content_type = ContentType.objects.get_for_model(self.model)
        ids = [
            node.pk for node, attributes, time in self.graph.edge_range(user, denounce, 0, count)
            if ContentType.objects.get_for_model(node) == content_type
        ]
        return self.get_queryset().filter(pk__in=ids)