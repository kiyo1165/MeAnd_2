from django.urls import path
from django.views.generic import TemplateView
from .views import Json, index

app_name = 'evaluation'
urlpatterns = [
    path('vue_test/', TemplateView.as_view(template_name='evaluation/test.html')),
    path('star/', Json.as_view(), name='vue_test'),
    path('test_index/', index, name='test_index')
]