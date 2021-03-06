# coding=utf-8
from django.db.models.signals import post_syncdb
import models as content_interactions_app


def create_edge_types(**kwargs):
    from social_graph.models import EdgeType, EdgeTypeAssociation
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
        FAVORITE_OF_STR,
        DENOUNCE,
        DENOUNCE_STR,
        DENOUNCED_BY,
        DENOUNCED_BY_STR,
        AUTHOR,
        AUTHOR_STR,
        AUTHORED_BY,
        AUTHORED_BY_STR,
        TARGET,
        TARGET_STR,
        TARGETED_BY,
        TARGETED_BY_STR,
    )
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

    # Denounce edges
    denounce, created = EdgeType.objects.get_or_create(name=DENOUNCE, defaults={
        'read_as': DENOUNCE_STR
    })
    denounced_by, created = EdgeType.objects.get_or_create(name=DENOUNCED_BY, defaults={
        'read_as': DENOUNCED_BY_STR
    })
    EdgeTypeAssociation.objects.get_or_create(direct=denounce, inverse=denounced_by)

    # Comment edges
    author, created = EdgeType.objects.get_or_create(name=AUTHOR, defaults={
        'read_as': AUTHOR_STR
    })
    authored_by, created = EdgeType.objects.get_or_create(name=AUTHORED_BY, defaults={
        'read_as': AUTHORED_BY_STR
    })
    EdgeTypeAssociation.objects.get_or_create(direct=author, inverse=authored_by)

    target, created = EdgeType.objects.get_or_create(name=TARGET, defaults={
        'read_as': TARGET_STR
    })
    targeted_by, created = EdgeType.objects.get_or_create(name=TARGETED_BY, defaults={
        'read_as': TARGETED_BY_STR
    })
    EdgeTypeAssociation.objects.get_or_create(direct=target, inverse=targeted_by)


post_syncdb.connect(create_edge_types, sender=content_interactions_app)