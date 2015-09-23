# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
import views

urlpatterns = patterns('',
    url(
        r'^like/$',
        login_required(views.LikeView.as_view()),
        name="like_item"
    ),

    url(
        r'^favorite/$',
        login_required(views.FavoriteView.as_view()),
        name="favorite_item"
    ),

    url(
        r'^share/$',
        login_required(views.ShareView.as_view()),
        name="share_item"
    ),

    url(
        r'^rate/$',
        login_required(views.RateView.as_view()),
        name="rate_item"
    ),

    url(
        r'^commented_rate/$',
        login_required(views.RateView.as_view(
            template_name = 'content_interactions/commented_rate.html'
        )),
        name="commented_rate_item"
    ),

    url(
        r'^denounce/$',
        login_required(views.DenounceView.as_view()),
        name="denounce_item"
    ),

    url(
        r'^comment/(?P<content_type_pk>\d+)/(?P<object_pk>\d+)/create/$',
        views.CommentCreateView.as_view(),
        name="comment_item"
    ),

    url(
        r'^comment/(?P<content_type_pk>\d+)/(?P<object_pk>\d+)/(?P<comment_pk>\d+)/answer/$',
        views.CommentCreateView.as_view(),
        name="comment_answer"
    ),

    url(
        r'^comment/(?P<content_type_pk>\d+)/(?P<object_pk>\d+)/list/$',
        views.CommentListView.as_view(),
        name="comment_list"
    ),

    url(
        r'^comment/(?P<pk>\d+)/edit/$',
        login_required(views.CommentUpdateView.as_view()),
        name="comment_edit"
    ),

    url(
        r'^comment/(?P<pk>\d+)/delete/$',
        login_required(views.CommentDeleteView.as_view()),
        name="comment_delete"
    ),
)