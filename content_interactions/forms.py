import time

from django.conf import settings
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.utils.crypto import salted_hmac, constant_time_compare
from django.forms.util import ErrorList, ErrorDict
from django.utils.translation import ugettext_lazy as _, ungettext, ugettext
from django.utils.text import get_text_list
from models import Comment


class ShareForm(forms.Form):
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=forms.HiddenInput())
    object_pk = forms.IntegerField(widget=forms.HiddenInput())
    addressee = forms.CharField(max_length=5000)
    comment = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 4}), required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False):
        super(ShareForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                        empty_permitted)
        content_type = initial.get('content_type', None)
        object_pk = initial.get('object_pk', None)
        if content_type and object_pk:
            self.object = content_type.get_object_for_this_type(pk=object_pk)

    def clean_addressee(self):
        addressee = self.cleaned_data['addressee']
        self.addressee_list = addressee.split(',')
        return addressee


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
            self._errors['comment'] = self.error_class(["This file is required."])
        return self.cleaned_data

    def save_denounce(self):
        if not self.obj.denounced_by(self.user):
            self.obj.denounce(self.user, self.cleaned_data['comment'])
            return True
        else:
            self.obj.remove_denounce(self.user)
            return False


DEFAULT_COMMENTS_TIMEOUT = getattr(settings, 'COMMENTS_TIMEOUT', (2 * 60 * 60))


class CommentForm(forms.ModelForm):
    timestamp = forms.IntegerField(widget=forms.HiddenInput)
    security_hash = forms.CharField(min_length=40, max_length=40, widget=forms.HiddenInput)
    honeypot = forms.CharField(
        required=False,
        label=_('If you enter anything in this field your comment will be treated as spam')
    )

    class Meta(object):
        model = Comment
        fields = ('content_type', 'object_pk', 'site', 'user', 'user_name', 'user_email', 'comment', 'answer_to')
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_pk': forms.HiddenInput(),
            'site': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'answer_to': forms.HiddenInput(),
        }

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None):
        if not instance:
            self._initial_validate(initial)
        initial.update(self._generate_security_data(instance or initial))
        super(CommentForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                          empty_permitted, instance)

    def _initial_validate(self, initial):
        if not 'content_type' in initial:
            raise ImproperlyConfigured(
                'Expect "content_type" within initial to initialize content_interactions.forms.CommentForm.'
            )

        if not 'object_pk' in initial:
            raise ImproperlyConfigured(
                'Expect "object_pk" within initial to initialize content_interactions.forms.CommentForm.'
            )

    def _generate_security_data(self, content):
        """Generate a dict of security data for "initial" data."""
        content_type = str(content.content_type.pk if isinstance(content, Comment) else content.get('content_type').pk)
        object_pk = str(content.object_pk if isinstance(content, Comment) else content.get('object_pk'))
        timestamp = str(int(time.time()))

        security_dict = {
            'timestamp': timestamp,
            'security_hash': self._generate_security_hash(content_type, object_pk, timestamp)
        }
        return security_dict

    def _generate_security_hash(self, content_type, object_pk, timestamp):
        """
        Generate a HMAC security hash from the provided info.
        """
        return salted_hmac(
            key_salt="content_interactions.forms.CommentForm",
            value="-".join([content_type, object_pk, timestamp])
        ).hexdigest()

    def clean_comment(self):
        """
        If COMMENTS_ALLOW_PROFANITIES is False, check that the comment doesn't
        contain anything in PROFANITIES_LIST.
        """
        comment = self.cleaned_data["comment"]
        if (not getattr(settings, 'COMMENTS_ALLOW_PROFANITIES', False) and
                getattr(settings, 'PROFANITIES_LIST', False)):
            bad_words = [w for w in settings.PROFANITIES_LIST if w in comment.lower()]
            if bad_words:
                raise forms.ValidationError(ungettext(
                    "Watch your mouth! The word %s is not allowed here.",
                    "Watch your mouth! The words %s are not allowed here.",
                    len(bad_words)) % get_text_list(
                    ['"%s%s%s"' % (i[0], '-' * (len(i) - 2), i[-1])
                     for i in bad_words], ugettext('and')))
        return comment

    def clean_security_hash(self):
        """Check the security hash."""
        security_hash_dict = {
            'content_type': self.data.get("content_type", ""),
            'object_pk': self.data.get("object_pk", ""),
            'timestamp': self.data.get("timestamp", ""),
        }
        expected_hash = self._generate_security_hash(**security_hash_dict)
        actual_hash = self.cleaned_data["security_hash"]
        if not constant_time_compare(expected_hash, actual_hash):
            raise forms.ValidationError(_(u"Security hash check failed."))
        return actual_hash

    def clean_timestamp(self):
        """Make sure the timestamp isn't too far (default is > 2 hours) in the past."""
        timestamp = self.cleaned_data["timestamp"]
        if time.time() - timestamp > DEFAULT_COMMENTS_TIMEOUT:
            raise forms.ValidationError(_(u"Timestamp check failed"))
        return timestamp

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value

    def clean_user_name(self):
        value = self.cleaned_data['user_name']
        if not value and not self.cleaned_data['user']:
            raise forms.ValidationError(_(u"This field is required."))
        return value

    def clean_user_email(self):
        value = self.cleaned_data['user_email']
        if not value and not self.cleaned_data['user']:
            raise forms.ValidationError(_(u"This field is required."))
        return value