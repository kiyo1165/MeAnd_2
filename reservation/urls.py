from django.urls import path
from .views import StaffCalendar, UserList, PlanList

app_name='reservation'
urlpatterns = [
    path('', UserList.as_view(), name='user_list'),
    path('<int:pk>/plan_list/', PlanList.as_view(), name='plan_list' ),
    path('<int:pk>/staff/', StaffCalendar.as_view(), name='calendar'),
    path('staff/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', StaffCalendar.as_view(), name='next_calendar'),
]
