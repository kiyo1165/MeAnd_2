from django.db import models
from accounts.models import User
from category.models import Category
from .choices_file import PLAN_TYPE_SELECT, COUNSELING_STYLE_CHOICES, COUNSELING_ACTIVE
# Create your models here.

class StyleChoices( models.Model ):
    style_name = models.CharField( max_length=10, blank=True )

    def __str__(self):
        return self.style_name

class Pref(models.Model):
    pref_name = models.CharField( max_length=6, blank=True, null=True )
    pref_code = models.CharField( max_length=2, blank=True, null=True )

    def __str__(self):
        return self.pref_name

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=100)
    catch_message = models.TextField('アイキャッチメッセージ', max_length=200,help_text='ヒント！ご相談される方が最初に見るメッセージです。')
    detail = models.TextField('本文', max_length=1000)
    target = models.CharField('対象者', max_length=100)
    plan_type = models.CharField('プランタイプ', max_length=20, choices=PLAN_TYPE_SELECT)
    price = models.CharField('価格', max_length=10)
    session_time = models.CharField('カウンセリング時間/一回', max_length=3, help_text='ヒント！分でご記入ください')
    style_choices = models.ManyToManyField(StyleChoices, related_name='style')
    counseling_active = models.CharField('カウンセリングのタイミング',max_length=20, choices=COUNSELING_ACTIVE)
    pref = models.ManyToManyField(Pref, related_name='pref', blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.title





