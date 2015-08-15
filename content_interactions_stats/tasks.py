# coding=utf-8
from celery import shared_task


@shared_task(name='content_interactions.like_process')
def item_like_process(item_id, item_content_type):
    from content_interactions_stats.utils import item_like_process
    item_like_process(item_id, item_content_type)


@shared_task(name='content_interactions.dislike_process')
def item_dislike_process(item_id, item_content_type):
    from content_interactions_stats.utils import item_dislike_process
    item_dislike_process(item_id, item_content_type)


@shared_task(name='content_interactions.new_rating_process')
def item_new_rating_process(item_id, item_content_type, rating):
    from content_interactions_stats.utils import item_new_rating_process
    item_new_rating_process(item_id, item_content_type, rating)


@shared_task(name='content_interactions.update_rating_process')
def item_updated_rating_process(item_id, item_content_type, old_rating, rating):
    from content_interactions_stats.utils import item_updated_rating_process
    item_updated_rating_process(item_id, item_content_type, old_rating, rating)


@shared_task(name='content_interactions.mark_favorite_process')
def item_marked_favorite_process(item_id, item_content_type):
    from content_interactions_stats.utils import item_marked_favorite_process
    item_marked_favorite_process(item_id, item_content_type)


@shared_task(name='content_interactions.unmark_favorite_process')
def item_unmarked_favorite_process(item_id, item_content_type):
    from content_interactions_stats.utils import item_unmarked_favorite_process
    item_unmarked_favorite_process(item_id, item_content_type)


@shared_task(name='content_interactions.share_process')
def item_shared_process(item_id, item_content_type):
    from content_interactions_stats.utils import item_shared_process
    item_shared_process(item_id, item_content_type)


@shared_task(name='content_interactions.denounce_process')
def item_denounced_process(item_id, item_content_type):
    from content_interactions_stats.utils import item_denounced_process
    item_denounced_process(item_id, item_content_type)


@shared_task(name='content_interactions.denounce_removed_process')
def item_denounce_removed_process(item_id, item_content_type):
    from content_interactions_stats.utils import item_denounce_removed_process
    item_denounce_removed_process(item_id, item_content_type)


@shared_task(name='content_interactions.visit_process')
def item_visited_process(item_id, item_content_type):
    from content_interactions_stats.utils import item_visited_process
    item_visited_process(item_id, item_content_type)

