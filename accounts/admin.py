from django.contrib import admin
from .models import User, Profile  # 追加

admin.site.register( User)
admin.site.register( Profile)