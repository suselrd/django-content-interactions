# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
import views

urlpatterns = patterns(
    '',
    url(
        r'^recent_activity/$',
        login_required(views.RecentActivityView.as_view()),
        name="recent_activity"
    ),
    url(
        r'^activity/$',
        login_required(views.AllActivityView.as_view()),
        name="activity"
    ),
)