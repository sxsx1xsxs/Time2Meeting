from django.db import models

# Create your models here.
class Events(models.Model):
    event_name = models.CharFiled(max_length=300)
    event_organizer = models.CharField(max_length=300)

class TimeSlots(model.Model):
    evetn_id = models.IntegerField(primary_key=True)
    event_participants = models.CharField(primary_key=True)
    timesolts_date = models.DateTimeField(None, None,False, False)
