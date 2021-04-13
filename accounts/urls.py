from django.urls import path
from django.urls import path
from .views \
    import ProfileEdit, MyProfile,\
    MyPageCalendar,MyPageDayDetail,\
    MyPageSchedule,MyPageScheduleDelete, my_page_holiday_add,my_page_day_holiday_add,my_page_day_holiday_delete,\
    CounselorGuidance,CounselorRegister,CounselorConfirmRegistered, MyPageMixin, ReservationList, BankRegister, BankRegisterUpdate,BankRegisterDetail

app_name = 'accounts'
urlpatterns = [
    path('mypage/', MyPageMixin.as_view(), name='mypage'), #管理画面テスト
    path('mypage/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/',MyPageMixin.as_view(), name='my_page_calendar3'),#管理画面テスト
    path( 'mypage/holiday/day/add/<int:pk>/<int:year>/<int:month>/<int:day>/', my_page_day_holiday_add,
          name='my_page_day_holiday_add' ),
    path( 'mypage/holiday/day/delete/<int:pk>/<int:year>/<int:month>/<int:day>/', my_page_day_holiday_delete,
          name='my_page_day_holiday_delete' ),
    path( 'my_page/<int:pk>/config/<int:year>/<int:month>/<int:day>/', MyPageDayDetail.as_view(),
          name='my_page_day_detail' ),
    path('cons_guidance/', CounselorGuidance.as_view(), name='counselor_guidance'),
    path('cons_register/', CounselorRegister.as_view(), name='counselor_register'),
    path('cons_confirm_registered/<int:pk>', CounselorConfirmRegistered.as_view(), name='cons_confirm_registered'),
    path('profile_edit/', ProfileEdit, name='profile_edit' ),
    path('profile/', MyProfile.as_view(), name='profile'),
    path('my_page/<int:pk>/calendar/', MyPageCalendar.as_view(), name='my_page_calendar'),
    path('my_page/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/',MyPageCalendar.as_view(), name='my_page_calendar2'),
    path('my_page/schedule/<int:pk>/', MyPageSchedule.as_view(), name='my_page_schedule'),
    path('my_page/schedule/<int:pk>/delete/', MyPageScheduleDelete.as_view(), name='my_page_schedule_delete'),
    path('mypage/holiday/add/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/',my_page_holiday_add, name='my_page_holiday_add'),
    path('mypage/reservation_list/', ReservationList.as_view(), name='reservation_list'),
    path('mypage/bank_register/', BankRegister.as_view(), name='bank_register'),
    path('mypage/bank_detail/', BankRegisterDetail.as_view(), name='bank_register_detail'),
    path('mypage/<int:pk>/bank_register_update/', BankRegisterUpdate.as_view(), name='bank_register_update'),



]
