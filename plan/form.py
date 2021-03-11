from django.forms import ModelForm
from .models import Plan, StyleChoices
from django import forms
from .choices_file import COUNSELING_STYLE_CHOICES

class PlanForm(ModelForm):
    title = forms.CharField(
        label='タイトル',
        widget=forms.Textarea(attrs={'rows': 3, 'cols':50,
                                     'class':'form-control',
                                     'placeholder': '100文字以内で記載してください。' })
    )
    catch_message = forms.CharField(
        label='アイキャッチメッセージ',
        widget=forms.Textarea(
            attrs={'rows': 4, 'cols':50,
                   'class':'form-control',
                   'placeholder': '200文字以内でプランの要約やご相談者へのメッセージを記載してください。'})
    )
    detail = forms.CharField(
        label='プラン詳細',
        widget=forms.Textarea(
            attrs={'rows': 10, 'cols':50,
                   'class':'form-control',
                   'placeholder': '1000文字以内でプランの要約やご相談者へのメッセージを記載してください。'})
        )
    target = forms.CharField(
        label='対象者',
        widget=forms.Textarea(
            attrs={'rows': 2, 'cols':50,
               'class': 'form-control',
               'placeholder': '100文字以内で対象者を記載してください。'})
    )
    price = forms.CharField(
        label='価格',
        widget=forms.TextInput(
            attrs={
                   'class': 'form-control',
                   'placeholder': '半角数字'} )
    )
    session_time = forms.CharField(
        label='カウンセリング時間/一回',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '分単位/例:1時間 => 60'} )
    )

    style_choices = forms.ModelMultipleChoiceField(queryset=StyleChoices.objects.all(),widget=forms.CheckboxSelectMultiple)



    class Meta:
        model = Plan
        exclude = ['created_at', 'updated_at', 'user']

