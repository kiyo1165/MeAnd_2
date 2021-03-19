from django.db import models
from django.utils import timezone
from accounts.models import User
from plan.models import Plan

# Create your models here.
#TODO planロジック変更
class Reservation(models.Model):
    """予約スケジュール."""
    start = models.DateTimeField('開始時間')
    end = models.DateTimeField('終了時間')
    message = models.CharField('メッセージ', max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='guest_user')
    user2 = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='host_user')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True, related_name='reserve_plan')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.message} {start} ~ {end} {self.user2}'


class ReservationMessage(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey( User, on_delete=models.CASCADE )
    message = models.TextField('メッセージ', max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message