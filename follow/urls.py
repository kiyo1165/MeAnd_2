from django.urls import path
from django.views.generic import TemplateView
from .views import FollowView

app_name = 'follow'
urlpatterns = [
    path('follow/', FollowView, name='follow' ),
    ]