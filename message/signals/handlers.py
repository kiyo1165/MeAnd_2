from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import request_finished
from  ..models import Message
from django.core.mail import send_mail

@receiver(post_save, sender=Message)
def message(sender, instance, created, **kwargs):
    if created and instance.user.email:
        print(kwargs)
        print(sender)
        send_mail(
                subject=f'【{instance.user_2.profile.nick_name}さんからメッセージ】MeAnd' ,
                message=f'{instance.send_text}',
                recipient_list=[ instance.user.email,],
                from_email='admin@example.com'
            )