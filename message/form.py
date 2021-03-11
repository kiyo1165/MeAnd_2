from django.forms import ModelForm
from .models import Message


class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Message
        fields = ['send_text']




