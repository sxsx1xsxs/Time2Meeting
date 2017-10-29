from django.contrib import admin
from .models import Events, Users, TimeSlots, EventUser

admin.site.register(Events)
admin.site.register(Users)
admin.site.register(TimeSlots)
admin.site.register(EventUser)
