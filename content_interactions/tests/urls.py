# coding=utf-8
from django.conf.urls import patterns, url, include
from django.views.generic import DetailView
from models import A


urlpatterns = patterns(
    "",
    url(r"(?P<pk>\d+)", DetailView.as_view(model=A),
        name="detail"),
    (r'^content_interactions/', include('content_interactions.urls')),
    (r'^monitoring/', include('content_interactions_monitoring.urls')),

)


