from django.db import models
from django.utils import timezone


# Create your models here.
class Events(models.Model):
    event_name = models.CharField(max_length=300, null=False)
    time_range_start = models.DateTimeField()
    time_range_end = models.DateTimeField(None, None, False, False)
    #event_organizer = models.CharField(max_length=300)
    wait_for_decision = models.BooleanField(default=True)
    deadline = models.DateTimeField(None, None, False, False)
    final_decision = models.BooleanField(default=False)
    #final_decision_timeslot = models.DateTimeField(None, None, False, False)

    # for inviting participants
    # participants = models.IntegerField()

    def __str__(self):
        return self.event_name

    #def is_wait_for_decision(self):
    #    now = timezone.now()
    #    if now >= self.deadline:
    #        self.wait_for_decision = True
    #        return True
    #    else:
    #        return False

    def generate_url(self):
        return True


class Users(models.Model):
    user_name = models.CharField(max_length=300)
    user_email = models.CharField(max_length=300)

    def __str__(self):
        return self.user_name


class TimeSlots(models.Model):
    #two fields are primary key together

    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    #event_participant = models.ForeignKey(Users, on_delete=models.CASCADE)

    timeslot = models.DateTimeField(None, None, False, False)
    is_result = models.IntegerField(default=0)
    is_decision = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.timeslot

class Results(models.Model):

    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    timeslot = models.DateTimeField(None, None, False, False)


class Decision(models.Model):

    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    timeslot = models.DateTimeField(None, None, False, False)

class Cell(models.Model)
