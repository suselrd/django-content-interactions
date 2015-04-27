# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import LikeView, FavoriteView, ShareView, RateView, DenounceView

urlpatterns = patterns('',
    url(
        r'^like/$',
        login_required(LikeView.as_view()),
        name="like_item"
    ),

    url(
        r'^favorite/$',
        login_required(FavoriteView.as_view()),
        name="favorite_item"
    ),

    url(
        r'^share/$',
        login_required(ShareView.as_view()),
        name="share_item"
    ),

    url(
        r'^rate/$',
        login_required(RateView.as_view()),
        name="rate_item"
    ),

    url(
        r'^commented_rate/$',
        login_required(RateView.as_view(
            template_name = 'content_interactions/commented_rate.html'
        )),
        name="commented_rate_item"
    ),
    url(
        r'^denounce/$',
        login_required(DenounceView.as_view()),
        name="denounce_item"
    ),
)