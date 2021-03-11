from django.urls import path
from .views import SendMessage, MessageList


app_name = 'message'

urlpatterns = [
    path('message_list/', MessageList.as_view(), name='message_list'),
    path('send_message/<int:pk>', SendMessage.as_view(), name='send_message'),

]