from django.urls import path
from .views import ProfileEdit, MyPage, MyProfile, ProfileCreate

app_name = 'accounts'
urlpatterns = [
    path('profile_create/', ProfileCreate, name='profile_create'),
    path('profile_edit/', ProfileEdit, name='profile_edit' ),
    path('my_page/', MyPage.as_view(), name='my_page'),
    path('profile/', MyProfile.as_view(), name='profile')
]
