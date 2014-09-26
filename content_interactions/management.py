# coding=utf-8
from django.db.models.signals import post_syncdb
from social_graph import EdgeType, EdgeTypeAssociation, models as social_graph_app
from . import (
    LIKE,
    LIKE_STR,
    LIKED_BY,
    LIKED_BY_STR,
    RATE,
    RATE_STR,
    RATED_BY,
    RATED_BY_STR,
    FAVORITE,
    FAVORITE_STR,
    FAVORITE_OF,
    FAVORITE_OF_STR
)


def create_edge_types(**kwargs):
    # Like edges
    like, created = EdgeType.objects.get_or_create(name=LIKE, defaults={
        'read_as': LIKE_STR
    })
    liked_by, created = EdgeType.objects.get_or_create(name=LIKED_BY, defaults={
        'read_as': LIKED_BY_STR
    })
    EdgeTypeAssociation.objects.get_or_create(direct=like, inverse=liked_by)

    # Rate edges
    rate, created = EdgeType.objects.get_or_create(name=RATE, defaults={
        'read_as': RATE_STR
    })
    rated_by, created = EdgeType.objects.get_or_create(name=RATED_BY, defaults={
        'read_as': RATED_BY_STR
    })
    EdgeTypeAssociation.objects.get_or_create(direct=rate, inverse=rated_by)

    # Favorite edges
    favorite, created = EdgeType.objects.get_or_create(name=FAVORITE, defaults={
        'read_as': FAVORITE_STR
    })
    favorite_of, created = EdgeType.objects.get_or_create(name=FAVORITE_OF, defaults={
        'read_as': FAVORITE_OF_STR
    })
    EdgeTypeAssociation.objects.get_or_create(direct=favorite, inverse=favorite_of)


post_syncdb.connect(create_edge_types, sender=social_graph_app)