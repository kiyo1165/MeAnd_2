from django.db import models
from django.utils import timezone
from accounts.models import User
import datetime
from plan.models import Plan
from .choise import STATUS_LIST
from plan.models import StyleChoices


# Create your models here.
class Reservation(models.Model):
    """予約スケジュール."""
    start = models.DateTimeField('開始時間')
    end = models.DateTimeField('終了時間')
    active = models.BooleanField('稼働可否',default=True) #休暇設定時にTrue
    message = models.CharField('メッセージ', max_length=255)
    status = models.CharField('ステータス', max_length=20, blank=True, choices=STATUS_LIST)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='guest_user')
    user2 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='host_user')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True, related_name='reserve_plan')
    style_choice = models.ManyToManyField(StyleChoices, verbose_name='面談スタイル', related_name='reserve_style_choice')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        start = timezone.make_aware(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.make_aware(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.message} {start} ~ {end} {self.user2}'

class ReservationMessage(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey( User, on_delete=models.CASCADE)
    message = models.TextField('メッセージ', max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
