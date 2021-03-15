from django.forms import ModelForm
from .models import Reservation
from django import forms

class BookingForm(ModelForm):
    message = forms.CharField(
        label='事前に相談したいメッセージ',

        widget=forms.Textarea(
            attrs={'rows':5, 'cols': 50,
                   'class': 'form-control',
                   'placeholder': '500文字以内'})
    )

    class Meta:
        model = Reservation
        fields = ('message',)


