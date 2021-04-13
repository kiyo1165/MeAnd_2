from django.contrib import admin
from .models import User, Profile,CounselorRegister, Qualification, Bank


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'email']


admin.site.register( User, UserAdmin)
admin.site.register( Profile)
admin.site.register( CounselorRegister)
admin.site.register(Qualification)
admin.site.register(Bank)