from django.forms import ModelForm
from .models import Plan, StyleChoices
from django import forms
from django.core.exceptions import ValidationError
from .models import StyleChoices

from .choices_file import COUNSELING_STYLE_CHOICES


class PlanForm(ModelForm):

    style_choices = forms.ModelMultipleChoiceField(
        label='面談のスタイル',
        queryset=StyleChoices.objects.all(),
        widget=forms.CheckboxSelectMultiple)



    title = forms.CharField(
        label='タイトル',
        widget=forms.Textarea(attrs={'rows': 2, 'cols':70,
                                     'class':'form-control',
                                     'placeholder': '30文字以内で記載してください。' })
    )
    catch_message = forms.CharField(
        label='アイキャッチメッセージ',
        widget=forms.Textarea(
            attrs={'rows': 3, 'cols':70,
                   'class':'form-control',
                   'placeholder': '100文字以内でプランの要約やご相談者へのメッセージを記載してください。'})
    )
    detail = forms.CharField(
        label='プラン詳細',
        widget=forms.Textarea(
            attrs={'rows': 15, 'cols':70,
                   'class':'form-control',
                   'placeholder': '1000文字以内でプランの要約やご相談者へのメッセージを記載してください。'})
        )
    target = forms.CharField(
        label='対象者',
        widget=forms.Textarea(
            attrs={'rows': 2, 'cols':50,
               'class': 'form-control',
               'placeholder': '100文字以内で対象者を記載してください。例：中学生の子育てで悩んでいる方'})
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

    def clean(self):
        cleaned_data = super().clean()
        style_choices = cleaned_data.get('style_choices')
        instance = StyleChoices.objects.get(style_name='対面')
        pref = cleaned_data.get('pref')
        if instance in style_choices and not pref:
            raise forms.ValidationError(
            '対面を選択された場合は対面エリアを選択してください。')
        return cleaned_data

    class Meta:
        model = Plan
        exclude = ['created_at', 'updated_at', 'user']

