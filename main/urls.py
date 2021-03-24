from django.urls import path
from django.views.generic import TemplateView
from .views import CateSearch, CateSearchDone, PlanDetail, UserList, UserListJson

app_name = 'main'
urlpatterns = [
    path('home/', TemplateView.as_view(template_name='index.html') ,name='top' ),
    path('cate_search/', CateSearch.as_view(), name='cate_search'),
    path('cate_search_done/<str:name>', CateSearchDone.as_view(), name='cate_search_done'),
    path('main/<int:pk>/plan_detail/', PlanDetail.as_view(), name='plan_detail'),
    path('test/',TemplateView.as_view(template_name='main/test.html')),
    path('user_list/', UserList.as_view(), name='user_list'),
    # path('', UserListJson, name='user_list_json'),

]
