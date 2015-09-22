# coding=utf-8
from django.conf import settings

# comments
COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)
setattr(settings, 'COMMENT_MAX_LENGTH', COMMENT_MAX_LENGTH)

COMMENT_MAX_LEVELS = getattr(settings, 'COMMENT_MAX_LEVELS', 1)
setattr(settings, 'COMMENT_MAX_LEVELS', COMMENT_MAX_LEVELS)
