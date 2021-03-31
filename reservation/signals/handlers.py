from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import request_finished
from  ..models import Reservation
from django.core.mail import send_mail, send_mass_mail

@receiver(post_save, sender=Reservation)
def message(sender, instance, created, **kwargs):
    print(instance.message)
    if created :
        if  '休暇' in instance.message:
            pass
            # send_mail(
            #         subject='【予約完了】' + str(instance.start) + '〜' + str(instance.end),
            #         message='開始時間：' + str(instance.start) + '〜' + str(instance.end) + 'カウンセラー：' +
            #                 instance.user2.first_name,
            #         recipient_list=[ instance.user2.email,],
            #         from_email='admin@example.com'
            #     )
            # print(instance)
        else:
            to_host = ('【予約が入りました】'+ str(instance.start) + '〜' + str(instance.end),
                       '開始時間：' + str( instance.start ) + '〜' + str( instance.end ) + 'カウンセラー：' + instance.user2.first_name,
                       instance.user2.email,
                       'admin@example.com'
                       )
            to_guest = (
                    '【予約完了】' + str( instance.start ) + '〜' + str( instance.end ),
                    '開始時間：' + str( instance.start ) + '〜' + str( instance.end ) + 'カウンセラー：' + instance.user.first_name,
                    instance.user.email,
                    'admin@example.com'
            )
            send_mass_mail( (to_host, to_guest) )



