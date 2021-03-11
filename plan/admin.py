from django.contrib import admin
from .models import Plan, Pref,StyleChoices
# Register your models here.
admin.site.register(Plan)
admin.site.register(Pref)
admin.site.register(StyleChoices)