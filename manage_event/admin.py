from django.contrib import admin
from .models import Events, TimeSlots, EventUser

admin.site.register(Events)
admin.site.register(TimeSlots)
admin.site.register(EventUser)
