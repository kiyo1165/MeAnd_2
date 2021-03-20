from django.urls import path
from .views import PlanCreate, MyPagePlanDetail,PlanList, MyPagePlanUpdate, MyPagePlanDelete

app_name ='plan'
urlpatterns = [
    path('plan_create/', PlanCreate, name='plan_create'),
    path('<int:pk>/plan_detail/', MyPagePlanDetail.as_view(), name='mypage_plan_detail'),
    path('<int:pk>/plan_delete/', MyPagePlanDelete.as_view(), name='mypage_plan_delete' ),
    path('<int:pk>/plan_update/', MyPagePlanUpdate, name='mypage_plan_update' ),
    path('plan_list/', PlanList.as_view(), name='plan_list' ),
]