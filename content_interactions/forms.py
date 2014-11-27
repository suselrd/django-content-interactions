# coding=utf-8
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList


class ReferForm(forms.Form):
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=forms.HiddenInput())
    object_pk = forms.IntegerField(widget=forms.HiddenInput())
    addressee = forms.CharField(max_length=5000)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False):
        super(ReferForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                        empty_permitted)
        content_type = initial.get('content_type', None)
        object_pk = initial.get('object_pk', None)
        if content_type and object_pk:
            self.object = content_type.get_object_for_this_type(pk=object_pk)

    def clean_addressee(self):
        addressee = self.cleaned_data['addressee']
        self.addressee_list = addressee.split(',')
        return addressee


class ShareForm(ReferForm):
    pass


class RecommendForm(ReferForm):
    comment = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 4}))


class RateForm(forms.Form):
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=forms.HiddenInput())
    object_pk = forms.CharField(widget=forms.HiddenInput())
    rating = forms.IntegerField(widget=forms.HiddenInput(), min_value=1, max_value=5)
    comment = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 4}), required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False):
        super(RateForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                       empty_permitted)
        self.user = initial.get('user', None)

    def save_rating(self):
        obj = self.cleaned_data['content_type'].get_object_for_this_type(
            **{'pk': self.cleaned_data['object_pk']}
        )
        if obj.rated_by(self.user):
            obj.change_rate(self.user, self.cleaned_data['rating'], self.cleaned_data['comment'])
        else:
            obj.save_rate(self.user, self.cleaned_data['rating'], self.cleaned_data['comment'])


class DenounceForm(forms.Form):
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=forms.HiddenInput())
    object_pk = forms.CharField(widget=forms.HiddenInput())
    comment = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 4}), required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False):
        super(DenounceForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                           empty_permitted)
        self.user = initial.get('user', None)

    def clean(self):
        self.obj = self.cleaned_data['content_type'].get_object_for_this_type(
            **{'pk': self.cleaned_data['object_pk']}
        )
        if not self.obj.denounced_by(self.user) and not self.cleaned_data.get('comment', None):
            raise ValidationError('Denounce comment is mandatory.')
        return self.cleaned_data

    def save_denounce(self):
        if not self.obj.denounced_by(self.user):
            self.obj.denounce(self.user, self.cleaned_data['comment'])
            return True
        else:
            self.obj.remove_denounce(self.user)
            return False

