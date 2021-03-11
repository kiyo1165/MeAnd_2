from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Profile
from django import forms


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'created_at', 'updated_at']

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
