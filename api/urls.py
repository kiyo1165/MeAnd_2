from django.urls import path
from .views import ConsUserListApiView

urlpatterns = [
    path('accounts/',ConsUserListApiView.as_view() ),
]