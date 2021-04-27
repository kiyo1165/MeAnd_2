from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('plan_create', views.PlanViewSet)

app_name = 'plan_create_api'

urlpatterns = [
    path('', include(router.urls)),
    path('pref_list/', views.PrefList.as_view())
]