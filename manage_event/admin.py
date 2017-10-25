from django.contrib import admin
from .models import Events, Users, TimeSlots, Results, Decision

admin.site.register(Events)
admin.site.register(Users)
admin.site.register(TimeSlots)
admin.site.register(Results)
admin.site.register(Decision)