from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from stdimage.models import StdImageField
from .choise import SEX_SELECT, OCCUPATION_SELECT
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('accounts')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター
           参考サイト：https://narito.ninja/blog/detail/39/
        """
        return self.email


class Qualification(models.Model):
    qualification_name = models.CharField('保有資格',max_length=30, blank=True)

    def __str__(self):
        return self.qualification_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField('ニックネーム', max_length=255, help_text='カウンセラーにはニックネームが表示されます。')
    phone = models.CharField('お電話番号', max_length=15, blank=True, help_text='※お電話でのカウンセリングはお電話番号が必要です。')
    age = models.CharField('年齢', max_length=3, blank=True)
    gender = models.CharField('性別', max_length=5, blank=True, choices=SEX_SELECT)
    pref = models.CharField('お住まいの都道府県', max_length=5, blank=True, help_text='※対面でのカウンセリングは都道府県が必要です。')
    occupation = models.CharField('ご職業', max_length=10, blank=True, choices=OCCUPATION_SELECT)
    qualification = models.ManyToManyField(Qualification, '保持資格',max_length=100, blank=True)
    career = models.TextField('経歴', max_length=1000, blank=True)
    years_of_experience = models.CharField('カウンセラー経験年数', max_length=10, blank=True)
    self_introduction = models.TextField('自己紹介', max_length=1000, blank=True)
    face_image = StdImageField('顔写真',upload_to='media/face_image', blank=True, variations={
        'xl':(1000, 400),
        'large': (600, 400),
        'thumbnail': (100, 100, True),
        'medium': (300, 200),
        'small': (70, 70),
    })
    your_image = StdImageField('あなたのイメージ写真',upload_to='media/your_image', blank=True, variations={
        'xl': (1300, 400),
        'large': (600, 400),
        'thumbnail': (100, 100),
        'medium': (300, 200),
        'small': (70, 70),
    } )
    face_book = models.URLField('FaceBook_URL', max_length=300, blank=True)
    Twitter = models.URLField('Twitter_URL', max_length=300, blank=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.gender


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    return instance.profile.save()


class CounselorRegister(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identification = models.ImageField('本人確認書類',upload_to='media/identification')
    credentials = models.ImageField('資格証明書', upload_to='media/credentials')
    signature = models.CharField('署名', max_length=20)
    address = models.CharField('住所', max_length=255)
    agreement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.signature


class Bank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_code = models.CharField('銀行コード', max_length=3)
    branch_office_code = models.CharField('支店コード', max_length=5)
    account_no = models.CharField('口座番号', max_length=20)
    account_name = models.CharField('口座名義', max_length=255)

    def __str__(self):
        return self.account_name





