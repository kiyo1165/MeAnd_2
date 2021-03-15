from django.urls import path
from .views \
    import ProfileEdit, MyPage, MyProfile,\
    ProfileCreate, MyPageCalendar,MyPageDayDetail,\
    MyPageSchedule,MyPageScheduleDelete, my_page_holiday_add

app_name = 'accounts'
urlpatterns = [
    path('profile_create/', ProfileCreate, name='profile_create'),
    path('profile_edit/', ProfileEdit, name='profile_edit' ),
    path('my_page/', MyPage.as_view(), name='my_page'),
    path('profile/', MyProfile.as_view(), name='profile'),
    path('my_page/<int:pk>/calendar/', MyPageCalendar.as_view(), name='my_page_calendar'),
    path('my_page/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/',MyPageCalendar.as_view(), name='my_page_calendar'),
    path( 'my_page/<int:pk>/config/<int:year>/<int:month>/<int:day>/', MyPageDayDetail.as_view(),
          name='my_page_day_detail' ),
    path('my_page/schedule/<int:pk>/', MyPageSchedule.as_view(), name='my_page_schedule'),
    path('my_page/schedule/<int:pk>/delete/', MyPageScheduleDelete.as_view(), name='my_page_schedule_delete'),
    path('mypage/holiday/add/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/',my_page_holiday_add, name='my_page_holiday_add'),

]
