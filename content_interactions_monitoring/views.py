# coding=utf-8
import logging
from django.utils.module_loading import import_by_path
from django.views.generic import ListView
from models import ActivityRecord

logger = logging.getLogger(__name__)


class AllActivityView(ListView):
    model = ActivityRecord
    context_object_name = 'activity_records'
    object = None

    def get_queryset(self):
        model = import_by_path(self.request.GET['model'])
        pk = self.request.GET['pk']
        self.object = model.objects.get(pk=pk)
        try:
            return self.object.activity_records.all()
        except:
            return self.model.objects.none()

    def get_template_names(self):
        names = super(AllActivityView, self).get_template_names()
        names.insert(
            0,
            "%s/%s/%s%s.html" % (
                self.model._meta.app_label,
                self.object._meta.model_name,
                self.model._meta.model_name,
                self.template_name_suffix
            )
        )
        return names


class RecentActivityView(AllActivityView):

    def get_queryset(self):
        model = import_by_path(self.request.GET['model'])
        pk = self.request.GET['pk']
        self.object = model.objects.get(pk=pk)
        try:
            return self.object.activity_records.current()
        except:
            return self.model.objects.none()
