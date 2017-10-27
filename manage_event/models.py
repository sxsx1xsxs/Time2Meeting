from django.db import models
# Create your models here.
class Users(models.Model):
    user_email = models.EmailField(max_length=254, primary_key=True)
    user_name = models.CharField(max_length=300)

    def __str__(self):
        return self.user_name


class Events(models.Model):
    event_name = models.CharField(max_length=300)
    time_range_start = models.DateTimeField()
    time_range_end = models.DateTimeField()
    final_time_start = models.DateTimeField(null=True, blank=True)
    final_time_end = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField()
    duration = models.DurationField()
    info = models.TextField(null=True)

    def __str__(self):
        return self.event_name


class EventUser(models.Model):
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    user_email = models.ForeignKey(Users)

    class Meta:
        unique_together = ("event_id", "user_email")

    role = models.CharField(max_length=1)


class TimeSlots(models.Model):
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    user_email = models.ForeignKey(Users)

    class Meta:
        unique_together = ("event_id", "user_email")

    time_slot_start = models.DateTimeField()
