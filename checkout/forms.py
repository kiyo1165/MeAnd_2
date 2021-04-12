from django.forms import ModelForm
from .models import CheckOutList

class CheckOutForm(ModelForm):

    class Meta:
        fields = ('cancel_flag',)
        model = CheckOutList