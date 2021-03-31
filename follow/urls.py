from django.urls import path
from django.views.generic import TemplateView
from .views import FollowView

app_name = 'follow'
urlpatterns = [
    path('<int:pk>/follow/', FollowView, name='follow' ),
    ]