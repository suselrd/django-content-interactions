# coding=utf-8
from social_graph import object_visited
from handlers import (
    visit_handler
)


class BaseProcessor(object):
    handlers = None
    record_type = None
    expiration = None

    def __init__(self):
        super(BaseProcessor, self).__init__()
        from models import ActivityRecordType, ActivityRecord
        handlers = self.get_handlers()
        if handlers:
            for handler_code, signal, handler in handlers:
                def decorated_handler(*args, **kwargs):
                    item, user = handler(*args, **kwargs)
                    from mixins import MonitoringMixin
                    if isinstance(item, MonitoringMixin):
                        record_type, created = ActivityRecordType.objects.get_or_create(name=self.record_type, defaults={
                            'expiration': self.expiration
                        })
                        if (not created) and (record_type.expiration != self.expiration):
                            record_type.expiration = self.expiration
                            record_type.save()

                        ActivityRecord.objects.create(
                            item=item,
                            user=user if user.is_authenticated() else None,
                            type=record_type
                        )
                signal.connect(decorated_handler, dispatch_uid='%s_monitor' % handler_code, weak=False)

    def get_handlers(self):
        return self.handlers


class Visits(BaseProcessor):
    record_type = 'Item Visited'
    expiration = 60*3  # 3 min (180 seg)
    handlers = (
        ('item_visited', object_visited, visit_handler),
    )
