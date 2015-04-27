# coding=utf-8
from django.db.models import F


def item_like_process(item_id, item_content_type):
    from models import Stats
    stats_obj, created = Stats.objects.get_or_create(object_pk=item_id, content_type=item_content_type)
    stats_obj.likes = F('likes')+1
    stats_obj.save()


def item_dislike_process(item_id, item_content_type):
    from models import Stats
    stats_obj, created = Stats.objects.get_or_create(object_pk=item_id, content_type=item_content_type)
    if not created:
        stats_obj.likes = F('likes')-1
        stats_obj.save()


def item_new_rating_process(item_id, item_content_type, rating):
    from models import Stats
    stats_obj, created = Stats.objects.get_or_create(object_pk=item_id, content_type=item_content_type)
    stats_obj.ratings = F('ratings')+1
    if rating == 5:
        stats_obj.rating_5_count = F('rating_5_count')+1
    elif rating == 4:
        stats_obj.rating_4_count = F('rating_4_count')+1
    elif rating == 3:
        stats_obj.rating_3_count = F('rating_3_count')+1
    elif rating == 2:
        stats_obj.rating_2_count = F('rating_2_count')+1
    elif rating == 1:
        stats_obj.rating_1_count = F('rating_1_count')+1
    stats_obj.save()


def item_updated_rating_process(item_id, item_content_type, old_rating, rating):
    from models import Stats
    stats_obj, created = Stats.objects.get_or_create(object_pk=item_id, content_type=item_content_type)
    if not created and (old_rating != rating):
        # remove ald rating
        if old_rating == 5:
            stats_obj.rating_5_count = F('rating_5_count')-1
        elif old_rating == 4:
            stats_obj.rating_4_count = F('rating_4_count')-1
        elif old_rating == 3:
            stats_obj.rating_3_count = F('rating_3_count')-1
        elif old_rating == 2:
            stats_obj.rating_2_count = F('rating_2_count')-1
        elif old_rating == 1:
            stats_obj.rating_1_count = F('rating_1_count')-1
        # add new rating
        if rating == 5:
            stats_obj.rating_5_count = F('rating_5_count')+1
        elif rating == 4:
            stats_obj.rating_4_count = F('rating_4_count')+1
        elif rating == 3:
            stats_obj.rating_3_count = F('rating_3_count')+1
        elif rating == 2:
            stats_obj.rating_2_count = F('rating_2_count')+1
        elif rating == 1:
            stats_obj.rating_1_count = F('rating_1_count')+1
    elif created:
        stats_obj.ratings = F('ratings')+1
        # add new rating
        if rating == 5:
            stats_obj.rating_5_count = F('rating_5_count')+1
        elif rating == 4:
            stats_obj.rating_4_count = F('rating_4_count')+1
        elif rating == 3:
            stats_obj.rating_3_count = F('rating_3_count')+1
        elif rating == 2:
            stats_obj.rating_2_count = F('rating_2_count')+1
        elif rating == 1:
            stats_obj.rating_1_count = F('rating_1_count')+1

    stats_obj.save()


def item_marked_favorite_process(item_id, item_content_type):
    from models import Stats
    stats_obj, created = Stats.objects.get_or_create(object_pk=item_id, content_type=item_content_type)
    stats_obj.favorite_marks = F('favorite_marks')+1
    stats_obj.save()


def item_unmarked_favorite_process(item_id, item_content_type):
    from models import Stats
    stats_obj, created = Stats.objects.get_or_create(object_pk=item_id, content_type=item_content_type)
    if not created:
        stats_obj.favorite_marks = F('favorite_marks')-1
        stats_obj.save()


def item_shared_process(item_id, item_content_type):
    from models import Stats
    stats_obj, created = Stats.objects.get_or_create(object_pk=item_id, content_type=item_content_type)
    stats_obj.shares = F('shares')+1
    stats_obj.save()


def item_visited_process(item_id, item_content_type):
    from models import Stats
    stats_obj, created = Stats.objects.get_or_create(object_pk=item_id, content_type=item_content_type)
    stats_obj.visits = F('visits')+1
    stats_obj.save()


def item_denounced_process(item_id, item_content_type):
    from models import Stats
    stats_obj, created = Stats.objects.get_or_create(object_pk=item_id, content_type=item_content_type)
    stats_obj.denounces = F('denounces')+1
    stats_obj.save()


def item_denounce_removed_process(item_id, item_content_type):
    from models import Stats
    stats_obj, created = Stats.objects.get_or_create(object_pk=item_id, content_type=item_content_type)
    stats_obj.denounces = F('denounces')-1
    stats_obj.save()

