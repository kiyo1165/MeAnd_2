from django.db import models
from accounts.models import User
from plan.models import Plan
from django.utils import timezone
# Create your models here.


class CheckOutList(models.Model):
    vendor_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='vendor_user')
    buyer_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='buyer_user')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    plan_type = models.CharField('プランタイプ', max_length=255)
    amount = models.IntegerField('料金', max_length=200000)
    strip_id = models.CharField('購入情報', max_length=255)
    customer_id = models.CharField('stripe顧客ID', max_length=255, blank=True)
    done_flag = models.BooleanField('カウンセリング完了フラグ', default=False)
    cancel_flag = models.BooleanField('cancelフラグ', default=False)
    created_at = models.DateTimeField('契約日', default=timezone.now())

    def __str__(self):
        created_at = timezone.localtime(self.created_at).strftime('%Y/%m/%d %H:%M:%S')
        return f'契約者:{self.buyer_user.last_name}{self.buyer_user.first_name} 提供者:{self.vendor_user.last_name}{self.vendor_user.first_name}StripeID:{self.strip_id} 契約日：{created_at}'

