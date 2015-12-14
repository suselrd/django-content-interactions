# coding=utf-8
from django.conf import settings

CONTENT_INTERACTIONS_MONITORING_PROCESSORS = getattr(settings, 'CONTENT_INTERACTIONS_MONITORING_PROCESSORS', (
    'content_interactions_monitoring.processors.Visits',
))
