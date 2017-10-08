from django.db import models

# Create your models here.
class Events(models.Model):
    event_name = models.CharFiled(max_length=300)

class TimeSlots(model.Model):
    timesolts_date = models.TimeField()
