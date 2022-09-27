from django.contrib import admin

from .models import Event, Cause, Skill, Profile, Candidate

admin.site.register(Event)
admin.site.register(Cause)
admin.site.register(Skill)
admin.site.register(Profile)
admin.site.register(Candidate)
