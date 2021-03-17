from django.contrib import admin
from .models import User, Profile,CounselorRegister

admin.site.register( User)
admin.site.register( Profile)
admin.site.register( CounselorRegister)