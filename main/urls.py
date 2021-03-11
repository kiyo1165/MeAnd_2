from django.urls import path
from django.views.generic import TemplateView
from .views import CateSearch, CateSearchDone, PlanDetail

app_name = 'main'
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html') ),
    path('cate_search/', CateSearch.as_view(), name='cate_search'),
    path('cate_search_done/<str:name>', CateSearchDone.as_view(), name='cate_search_done'),
    path('<int:pk>/plan_detail/', PlanDetail.as_view(), name='plan_detail'),
    path('test/',TemplateView.as_view(template_name='main/test.html')),
]
