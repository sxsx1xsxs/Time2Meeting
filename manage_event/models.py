import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Module for profile.
    """
    user = models.OneToOneField(User, unique=True, null=False, db_index=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create user profile.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save user profile.
    """
    instance.profile.save()


class Events(models.Model):
    """
    Module for events table.
    """
    event_name = models.CharField(max_length=300, blank=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    time_range_start = models.DateTimeField(blank=False)
    time_range_end = models.DateTimeField()
    final_time_start = models.DateTimeField(null=True, blank=True)
    final_time_end = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField()
    duration = models.DurationField()

    # record the status of the event, "Available' or 'Abort'
    status = models.CharField(max_length=10, default='Available')
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.event_name


class AbortMessage(models.Model):
    """
    Module for abort message table.
    """
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    Abort_message = models.TextField(null=True, blank=True)


class EventUser(models.Model):
    """
    Module for eventuser table, which is used for record role of user.
    """
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True)

    class Meta:
        unique_together = ("event", "user")

    # two roles: "O" for organizer, "P" for participant
    USER_ROLE = (
        ('o', 'Organizer'),
        ('p', 'Participant'),
    )
    role = models.CharField(max_length=1, choices=USER_ROLE, default='p')


class TimeSlots(models.Model):
    """
    Module for time slots table.
    """
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True)
    time_slot_start = models.DateTimeField()

    class Meta:
        unique_together = ("event", "user", "time_slot_start")


class Invitation(models.Model):
    """
    Model for invitations.
    """
    email = models.EmailField(max_length=254)
    event = models.ForeignKey(Events)
    expired = models.BooleanField(default=False)

    class Meta:
        unique_together = ("email", "event")
