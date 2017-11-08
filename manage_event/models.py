from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Users(models.Model):
    user_email = models.EmailField(max_length=254, primary_key=True)
    user_name = models.CharField(max_length=300)

    def __str__(self):
        return self.user_name


class Events(models.Model):
    event_name = models.CharField(max_length=300)
    create_time = models.DateTimeField(default=timezone.now)
    time_range_start = models.DateTimeField()
    time_range_end = models.DateTimeField()
    final_time_start = models.DateTimeField(null=True, blank=True)
    final_time_end = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField()
    duration = models.DurationField()
    status = models.CharField(max_length=10, default='Available')
    # record the status of the event, "Available' or 'Abort'

    def clean(self):
        if self.time_range_start < timezone.now():
            raise ValidationError(_('invalid time range start point'))
        if self.time_range_end < self.time_range_start:
            raise ValidationError(_('invalid time range'))
        if self.deadline > self.time_range_start:
            raise ValidationError(_('invalid deadline'))
    info = models.TextField(null=True)

    def __str__(self):
        return self.event_name


class EventUser(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(Users)

    class Meta:
        unique_together = ("event", "user")

    role = models.CharField(max_length=1)


class TimeSlots(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(Users)

    class Meta:
        unique_together = ("event", "user")

    time_slot_start = models.DateTimeField()
