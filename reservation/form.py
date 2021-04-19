from django.forms import ModelForm
from .models import Reservation
from django import forms
from reservation.models import StyleChoices


class BookingForm(ModelForm):
    message = forms.CharField(
        label='事前に相談したいメッセージ',

        widget=forms.Textarea(
            attrs={'rows':5, 'cols': 50,
                   'class': 'form-control',
                   'placeholder': '500文字以内'})
    )
    style_choice = forms.ModelMultipleChoiceField(queryset=StyleChoices.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple )

    class Meta:
        model = Reservation
        fields = ('message','style_choice')


