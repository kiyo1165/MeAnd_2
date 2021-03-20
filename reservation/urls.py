from django.urls import path
from .views import StaffCalendar, UserList, Booking, BookingMessage

app_name='reservation'
urlpatterns = [
    path('', UserList.as_view(), name='user_list'),
    path('<int:pk>/staff/', StaffCalendar.as_view(), name='calendar'),
    path('staff/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', StaffCalendar.as_view(), name='next_calendar'),
    path('staff/<int:pk>/booking/<int:year>/<int:month>/<int:day>/<int:hour>/', Booking.as_view(), name='booking'),
    path('bookinng_message/<int:pk>',BookingMessage.as_view(),name='booking_message'),
]
