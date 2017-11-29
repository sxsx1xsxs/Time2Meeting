from django.contrib.auth.models import User
from manage_event.models import Profile, Events, AbortMessage
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import datetime
import re
from django.core.validators import validate_email
from datetimewidget.widgets import DateTimeWidget


class InvitationForm(forms.Form):
    emails = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 5, 'cols': 30, }))

    def clean(self):
        cleaned_data = super(InvitationForm, self).clean()
        emails = re.compile(r'[^\w.\-+@_]+').split(cleaned_data.get('emails'))

        for email in emails:
            validate_email(email)

        return emails


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date')


class AbortForm(forms.ModelForm):
    class Meta:
        model = AbortMessage
        fields = ('Abortion_message',)


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ('event_name', 'time_range_start', 'time_range_end', 'duration', 'deadline', 'info')
        dateTimeOptions = {
            'format': 'yyyy-mm-dd hh:ii',
            'minuteStep': 30,
            'showMeridian': True
        }

        DURATION = (
            ('30:00', '30 min'),
            ('1:00:00', '60 min'),
            ('1:30:00', '90 min'),
            ('2:00:00', '120 min'),
            ('2:30:00', '2.5 h'),
            ('3:00:00', '3 h'),
            ('3:30:00', '3.5 h'),
            ('4:00:00', '4 h'),
            ('4:30:00', '4.5 h'),
            ('5:00:00', '5 h'),
        )

        widgets = {
            'time_range_start': DateTimeWidget(bootstrap_version=2, options=dateTimeOptions),
            'time_range_end': DateTimeWidget(bootstrap_version=2, options=dateTimeOptions),
            'duration': forms.Select(choices=DURATION),
            'deadline': DateTimeWidget(bootstrap_version=2, options=dateTimeOptions),
            'info': forms.Textarea(attrs={'rows': 5, 'cols': 30})
        }
        help_texts = {
            'event_name': _('*No more than 300 characters.'),
            'info': _('(optional)'),
        }

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        time_range_start = cleaned_data.get('time_range_start')
        time_range_end = cleaned_data.get('time_range_end')
        duration = cleaned_data.get('duration')
        deadline = self.cleaned_data.get('deadline')

        error_list = []

        if duration > (time_range_end - time_range_start):
            error = forms.ValidationError(
                _("%(value1)s should be smaller than %(value2)s!"),
                code='smaller than',
                params={'value1': 'duration',
                        'value2': 'time range'})
            error_list.append(error)

        if time_range_start <= timezone.now():
            error = forms.ValidationError(
                _("%(value1)s should be later than %(value2)s!"),
                code='later than',
                params={'value1': 'time range start',
                        'value2': 'current time'})
            error_list.append(error)

        if time_range_start >= time_range_end:
            error = forms.ValidationError(
                _("%(value1)s should be later than %(value2)s!"),
                code='earlier than',
                params={'value1': 'time range start',
                        'value2': 'time range end'})
            error_list.append(error)

        if deadline > time_range_start:
            error = forms.ValidationError(
                _("%(value1)s should be earlier than %(value2)s!"),
                code='earlier than',
                params={'value1': 'deadline',
                        'value2': 'time range start'})
            error_list.append(error)

        if deadline <= timezone.now():
            error = forms.ValidationError(
                _("%(value1)s should be later than %(value2)s!"),
                code='later than',
                params={'value1': 'deadline',
                        'value2': 'current time'})
            error_list.append(error)

        if time_range_end > time_range_start + datetime.timedelta(days=7):
            error = forms.ValidationError(
                _("time range should be no more than %(value)s days!"),
                code='earlier than',
                params={'value': '7'})
            error_list.append(error)

        if error_list:
            raise forms.ValidationError(error_list)

