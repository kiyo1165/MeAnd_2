from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from accounts.models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
