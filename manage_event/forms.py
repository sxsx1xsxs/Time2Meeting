from django.contrib.auth.models import User
from manage_event.models import Profile
from manage_event.models import Events
from django import forms


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
        fields = ('event_name', 'time_range_start', 'time_range_end', 'deadline')
