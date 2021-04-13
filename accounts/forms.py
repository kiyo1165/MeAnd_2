from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Profile, Qualification, Bank
from reservation.models import Reservation
from allauth.account.forms import SignupForm
from django import forms
# from plan.models import StyleChoices

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ['user', 'created_at', 'updated_at']
        widgets ={
            'phone': forms.TextInput(attrs={
                'placeholder': '例：08012341234※ハイフンなしでご入力ください。'
            }),
        }



    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs )
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'



class CustomSignupForm(SignupForm):

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    def custom_signup(self, request, user):
        # Set the user's type from the form reponse
        user.type = self.cleaned_data["type"]
        # Save the user's type to their database record
        user.save()


class ReserveUpdateForm(ModelForm):
    start = forms.SplitDateTimeField(label='開始時間', widget=forms.SplitDateTimeWidget(date_attrs={'type':'date'},time_attrs={'type':'time'}))
    end = forms.SplitDateTimeField(label='終了時間', widget=forms.SplitDateTimeWidget(date_attrs={'type':'date'},time_attrs={'type':'time'}))

    class Meta:
        model = Reservation
        fields = ['start', 'end', 'message']


class BankRegisterForm(ModelForm):

    class Meta:
        model = Bank
        fields = [
            'bank_code',
            'branch_office_code',
            'account_no',
            'account_name',
        ]
        widgets = {
            'bank_code': forms.NumberInput(attrs={'placeholder': '0001'}),
            'branch_office_code': forms.NumberInput(attrs={'placeholder': '001'}),
            'account_no': forms.NumberInput(attrs={'placeholder': '7桁の半角英数字'}),
            'account_name': forms.TextInput(attrs={'placeholder': 'ヤマダ　タロウ'}),
        }
