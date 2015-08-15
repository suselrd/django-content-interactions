# coding=utf-8
from django.contrib.contenttypes.models import ContentType
from settings import (
    CONTENT_INTERACTIONS_LIKE_PROCESSING_DELAY,
    CONTENT_INTERACTIONS_RATE_PROCESSING_DELAY,
    CONTENT_INTERACTIONS_FAVORITE_PROCESSING_DELAY,
    CONTENT_INTERACTIONS_DENOUNCE_PROCESSING_DELAY,
    CONTENT_INTERACTIONS_SHARE_PROCESSING_DELAY,
    CONTENT_INTERACTIONS_VISIT_PROCESSING_DELAY
)


#noinspection PyUnresolvedReferences,PyUnusedLocal
def like_handler(instance, **kwargs):
    if CONTENT_INTERACTIONS_LIKE_PROCESSING_DELAY:
        try:
            from tasks import item_like_process
            item_like_process.delay(instance.pk, ContentType.objects.get_for_model(instance))
            return
        except ImportError:
            pass
    from utils import item_like_process as sync_item_like_process
    sync_item_like_process(instance.pk, ContentType.objects.get_for_model(instance))


#noinspection PyUnresolvedReferences,PyUnusedLocal
def dislike_handler(instance, **kwargs):
    if CONTENT_INTERACTIONS_LIKE_PROCESSING_DELAY:
        try:
            from tasks import item_dislike_process
            item_dislike_process.delay(instance.pk, ContentType.objects.get_for_model(instance))
            return
        except ImportError:
            pass
    from utils import item_dislike_process as sync_item_dislike_process
    sync_item_dislike_process(instance.pk, ContentType.objects.get_for_model(instance))


#noinspection PyUnresolvedReferences,PyUnusedLocal
def new_rating_handler(instance, rating, **kwargs):
    if CONTENT_INTERACTIONS_RATE_PROCESSING_DELAY:
        try:
            from tasks import item_new_rating_process
            item_new_rating_process.delay(instance.pk, ContentType.objects.get_for_model(instance), rating)
            return
        except ImportError:
            pass
    from utils import item_new_rating_process as sync_item_new_rating_process
    sync_item_new_rating_process(instance.pk, ContentType.objects.get_for_model(instance), rating)


#noinspection PyUnresolvedReferences,PyUnusedLocal
def updated_rating_handler(instance, rating, old_rating, **kwargs):
    if CONTENT_INTERACTIONS_RATE_PROCESSING_DELAY:
        try:
            from tasks import item_updated_rating_process
            item_updated_rating_process.delay(
                instance.pk, ContentType.objects.get_for_model(instance), old_rating, rating
            )
            return
        except ImportError:
            pass
    from utils import item_updated_rating_process as sync_item_updated_rating_process
    sync_item_updated_rating_process(instance.pk, ContentType.objects.get_for_model(instance), old_rating, rating)


#noinspection PyUnresolvedReferences,PyUnusedLocal
def update_cached_rating(instance, **kwargs):
    instance.rating = (
        5 * instance.rating_5_count
        + 4 * instance.rating_4_count
        + 3 * instance.rating_3_count
        + 2 * instance.rating_2_count
        + instance.rating_1_count
    )/(instance.ratings * float(1)) if instance.ratings else 0
    return instance


#noinspection PyUnresolvedReferences,PyUnusedLocal
def favorite_mark_handler(instance, **kwargs):
    if CONTENT_INTERACTIONS_FAVORITE_PROCESSING_DELAY:
        try:
            from tasks import item_marked_favorite_process
            item_marked_favorite_process.delay(instance.pk, ContentType.objects.get_for_model(instance))
            return
        except ImportError:
            pass
    from utils import item_marked_favorite_process as sync_item_marked_favorite_process
    sync_item_marked_favorite_process(instance.pk, ContentType.objects.get_for_model(instance))


#noinspection PyUnresolvedReferences,PyUnusedLocal
def favorite_unmark_handler(instance, **kwargs):
    if CONTENT_INTERACTIONS_FAVORITE_PROCESSING_DELAY:
        try:
            from tasks import item_unmarked_favorite_process
            item_unmarked_favorite_process.delay(instance.pk, ContentType.objects.get_for_model(instance))
            return
        except ImportError:
            pass
    from utils import item_unmarked_favorite_process as sync_item_unmarked_favorite_process
    sync_item_unmarked_favorite_process(instance.pk, ContentType.objects.get_for_model(instance))


#noinspection PyUnresolvedReferences,PyUnusedLocal
def denounce_handler(instance, **kwargs):
    if CONTENT_INTERACTIONS_DENOUNCE_PROCESSING_DELAY:
        try:
            from tasks import item_denounced_process
            item_denounced_process.delay(instance.pk, ContentType.objects.get_for_model(instance))
            return
        except ImportError:
            pass
    from utils import item_denounced_process as sync_item_denounced_process
    sync_item_denounced_process(instance.pk, ContentType.objects.get_for_model(instance))


#noinspection PyUnresolvedReferences,PyUnusedLocal
def denounce_remove_handler(instance, **kwargs):
    if CONTENT_INTERACTIONS_DENOUNCE_PROCESSING_DELAY:
        try:
            from tasks import item_denounce_removed_process
            item_denounce_removed_process.delay(instance.pk, ContentType.objects.get_for_model(instance))
            return
        except ImportError:
            pass
    from utils import item_denounce_removed_process as sync_item_denounce_removed_process
    sync_item_denounce_removed_process(instance.pk, ContentType.objects.get_for_model(instance))


#noinspection PyUnresolvedReferences,PyUnusedLocal
def share_handler(instance, **kwargs):
    if CONTENT_INTERACTIONS_SHARE_PROCESSING_DELAY:
        try:
            from tasks import item_shared_process
            item_shared_process.delay(instance.pk, ContentType.objects.get_for_model(instance))
            return
        except ImportError:
            pass
    from utils import item_shared_process as sync_item_shared_process
    sync_item_shared_process(instance.pk, ContentType.objects.get_for_model(instance))


#noinspection PyUnresolvedReferences,PyUnusedLocal
def visit_handler(instance, **kwargs):
    if CONTENT_INTERACTIONS_VISIT_PROCESSING_DELAY:
        try:
            from tasks import item_visited_process
            item_visited_process.delay(instance.pk, ContentType.objects.get_for_model(instance))
            return
        except ImportError:
            pass
    from utils import item_visited_process as sync_item_visited_process
    sync_item_visited_process(instance.pk, ContentType.objects.get_for_model(instance))