from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import request_finished
from  ..models import Reservation
from django.core.mail import send_mail

@receiver(post_save, sender=Reservation)
def message(sender, instance, created, **kwargs):
    if created and instance.user.email:
        send_mail(
                subject='【予約完了】' + str(instance.start) + '〜' + str(instance.end),
                message='開始時間：' + str(instance.start) + '〜' + str(instance.end) + 'カウンセラー：' +
                        instance.user.first_name,
                recipient_list=[ instance.user.email,],
                from_email='admin@example.com'
            )


