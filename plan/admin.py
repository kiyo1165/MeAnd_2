from django.contrib import admin
from .models import Plan, Pref, StyleChoices, City
# Register your models here.
admin.site.register(Plan)
admin.site.register(Pref)
admin.site.register(StyleChoices)
admin.site.register(City)
