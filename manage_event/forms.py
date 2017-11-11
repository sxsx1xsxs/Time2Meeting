from django.contrib.auth.models import User
from manage_event.models import Profile, Events
from django import forms
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date')


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ('event_name', 'time_range_start', 'time_range_end', 'duration', 'deadline')

    def clean(self):
        if self.time_range_start < timezone.now():
            raise ValidationError('invalid time range start point')
        if self.time_range_end < self.time_range_start:
            raise ValidationError('invalid time range')
        if self.deadline > self.time_range_start:
            raise ValidationError('invalid deadline')

