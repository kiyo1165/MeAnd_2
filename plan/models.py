from django.db import models
from accounts.models import User
from category.models import Category
from .choices_file import PLAN_TYPE_SELECT, COUNSELING_STYLE_CHOICES, COUNSELING_ACTIVE
from stdimage.models import StdImageField
# Create your models here.


class Pref(models.Model):
    pref_name = models.CharField( max_length=6, blank=True, null=True )
    pref_code = models.CharField( max_length=2, blank=True, null=True )

    def __str__(self):
        return self.pref_name


class StyleChoices(models.Model):
    style_name = models.CharField( max_length=10, blank=True )

    def __str__(self):
        return self.style_name


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=30)
    catch_message = models.TextField('アイキャッチメッセージ', max_length=100, help_text='ヒント！ご相談される方が最初に見るメッセージです。')
    detail = models.TextField('本文', max_length=1000)
    plan_sign = StdImageField( upload_to='media/plan_sign', blank=True, default='static/icon/MeAnd_Logo1.png', variations={
        'xl': (1000, 400),
        'large': (600, 400),
        'medium': (300, 200),
        'thumbnail':(200, 170)
    })
    target = models.CharField('対象者', max_length=100)
    plan_type = models.CharField('プランタイプ', max_length=20, choices=PLAN_TYPE_SELECT)
    price = models.CharField('価格', max_length=10)
    session_time = models.CharField('カウンセリング時間/一回', max_length=3, help_text='ヒント！分でご記入ください')
    counseling_active = models.CharField('カウンセリングのタイミング',max_length=20, blank=True, choices=COUNSELING_ACTIVE)
    pref = models.ManyToManyField(Pref, related_name='pref', blank=True)
    style_choices = models.ManyToManyField( StyleChoices, related_name='style' )
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    release = models.BooleanField('公開', default=False)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.title






