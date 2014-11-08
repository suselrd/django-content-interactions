# coding=utf-8
import json
import logging
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.encoding import force_text
from django.utils.module_loading import import_by_path
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, FormView
from .forms import ShareForm, RecommendForm, RateForm, DenounceForm
from .signals import item_shared, item_recommended
from .utils import intmin

logger = logging.getLogger(__name__)

MODAL_VALIDATION_ERROR_MESSAGE = _(u"A validation error has occurred.")
MODAL_SHARE_SUCCESS_MESSAGE = _(u"The item has been successfully shared.")
MODAL_RECOMMEND_SUCCESS_MESSAGE = _(u"The item has been successfully recommended.")
MODAL_RATE_SUCCESS_MESSAGE = _(u"The item has been successfully rated.")
MODAL_DENOUNCE_SUCCESS_MESSAGE = _(u"The item has been successfully denounced.")


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


class LikeView(JSONResponseMixin, View):

    def dispatch(self, request, *args, **kwargs):
        return super(LikeView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            model = import_by_path(request.POST['model'])
            pk = request.POST['pk']
            instance = model.objects.get(pk=pk)

            if instance.liked_by(request.user):
                instance.unlike(request.user)
                tooltip = _(u"Like")
                toggle_status = False
            else:
                instance.like(request.user)
                tooltip = _(u"Unlike")
                toggle_status = True

            likes = instance.likes

            return self.render_to_response({
                'result': True,
                'toggle_status': toggle_status,
                'counter': likes,
                'counterStr': intmin(likes),
                'tooltip': force_text(tooltip)
            })

        except MultiValueDictKeyError as e:
            logger.exception(e)
            return self.render_to_response({'result': False})
        except ImproperlyConfigured as e:
            logger.exception(e)
            return self.render_to_response({'result': False})
        except Exception as e:
            logger.exception(e)
            return self.render_to_response({'result': False})


class FavoriteView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            model = import_by_path(request.POST['model'])
            pk = request.POST['pk']
            instance = model.objects.get(pk=pk)

            if instance.favorite_of(request.user):
                instance.delete_favorite(request.user)
                tooltip = _(u"Mark as Favorite")
                toggle_status = True
            else:
                instance.mark_as_favorite(request.user)
                tooltip = _(u"Not my Favorite")
                toggle_status = True

            favorite_marks = instance.favorite_marks

            return self.render_to_response({
                'result': True,
                'toggle_status': toggle_status,
                'counter': favorite_marks,
                'counterStr': intmin(favorite_marks),
                'tooltip': force_text(tooltip)
            })

        except Exception as e:
            logger.exception(e)
            return self.render_to_response({'result': False})


class ShareView(FormView):
    template_name = 'content_interactions/share.html'
    form_class = ShareForm

    def get_initial(self):
        content_type_pk = self.request.REQUEST.get('content_type', None)
        return {
            'content_type': ContentType.objects.get(pk=content_type_pk) if content_type_pk else None,
            'object_pk': self.request.REQUEST.get('object_pk', None)
        }

    def form_valid(self, form):
        """
        If the form is valid, share item.
        """

        if form.object:
            item_shared.send(form.object.__class__,
                             instance=form.object,
                             user=self.request.user,
                             addressee_list=form.addressee_list)
        context = {
            'successMsg': force_text(MODAL_SHARE_SUCCESS_MESSAGE),
        }
        return HttpResponse(json.dumps(context), content_type='application/json')

    def form_invalid(self, form):
        context = {
            'errorMsg': force_text(MODAL_VALIDATION_ERROR_MESSAGE)
        }
        return HttpResponseBadRequest(json.dumps(context), content_type='application/json')


class RecommendView(FormView):
    template_name = 'content_interactions/recommend.html'
    form_class = RecommendForm

    def get_initial(self):
        content_type_pk = self.request.REQUEST.get('content_type', None)
        return {
            'content_type': ContentType.objects.get(pk=content_type_pk) if content_type_pk else None,
            'object_pk': self.request.REQUEST.get('object_pk', None)
        }

    def form_valid(self, form):
        """
        If the form is valid, share item.
        """
        if form.object:
            item_recommended.send(form.object.__class__,
                             instance=form.object,
                             user=self.request.user,
                             addressee_list=form.addressee_list,
                             comment=form.cleaned_data['comment'])
        context = {
            'successMsg': force_text(MODAL_RECOMMEND_SUCCESS_MESSAGE),
        }
        return HttpResponse(json.dumps(context), content_type='application/json')

    def form_invalid(self, form):
        context = {
            'errorMsg': force_text(MODAL_VALIDATION_ERROR_MESSAGE)
        }
        return HttpResponseBadRequest(json.dumps(context), content_type='application/json')


class RateView(FormView):
    template_name = 'content_interactions/rate.html'
    form_class = RateForm

    def get_initial(self):
        content_type_pk = self.request.GET.get('content_type', None)
        content_type = ContentType.objects.get_for_id(content_type_pk) if content_type_pk else None
        object_pk = self.request.GET.get('object_pk', None)
        # find the related model
        model = content_type.get_object_for_this_type(**{'pk': object_pk}) if content_type and object_pk else None
        return {
            'content_type': content_type,
            'object_pk': object_pk,
            'rating': model.rating(self.request.user) if model and model.rated_by(self.request.user) else self.request.GET.get('min_rate', 0),
            'user': self.request.user
        }

    def form_valid(self, form):
        """
        If the form is valid, save the rating associated with the model.
        """
        form.save_rating()
        context = {
            'successMsg': force_text(MODAL_RATE_SUCCESS_MESSAGE),
        }
        return HttpResponse(json.dumps(context), content_type='application/json')

    def form_invalid(self, form):
        context = {
            'errorMsg': force_text(MODAL_VALIDATION_ERROR_MESSAGE)
        }
        return HttpResponseBadRequest(json.dumps(context), content_type='application/json')


class DenounceView(FormView):
    template_name = 'content_interactions/denounce.html'
    form_class = DenounceForm

    def get_initial(self):
        content_type_pk = self.request.GET.get('content_type', None)
        content_type = ContentType.objects.get_for_id(content_type_pk) if content_type_pk else None
        object_pk = self.request.GET.get('object_pk', None)
        return {
            'content_type': content_type,
            'object_pk': object_pk,
            'user': self.request.user
        }

    def form_valid(self, form):
        """
        If the form is valid, toggle denounce status.
        """
        form.save_denounce()
        context = {
            'successMsg': force_text(MODAL_DENOUNCE_SUCCESS_MESSAGE),
        }
        return HttpResponse(json.dumps(context), content_type='application/json')

    def form_invalid(self, form):
        context = {
            'errorMsg': force_text(MODAL_VALIDATION_ERROR_MESSAGE)
        }
        return HttpResponseBadRequest(json.dumps(context), content_type='application/json')