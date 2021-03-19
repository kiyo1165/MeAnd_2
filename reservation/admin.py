from django.contrib import admin
from .models import Reservation, ReservationMessage
# Register your models here.
admin.site.register(Reservation)
admin.site.register(ReservationMessage)