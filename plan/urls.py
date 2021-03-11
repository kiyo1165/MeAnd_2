from django.urls import path
from .views import PlanCreate, PlanDetail

app_name ='plan'
urlpatterns = [
    path('plan_create/', PlanCreate, name='plan_create'),
    path('<int:pk>/plan_detail/', PlanDetail.as_view(), name='plan_detail'),
]