from django.db import models
from accounts.models import User
from django.utils import timezone


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='message_user')
    user_2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='message_user2')
    send_text = models.TextField('メッセージ', max_length=1000)
    created_at = models.DateTimeField('日付', auto_now_add=True)

    def __str__(self):
        return self.send_text
