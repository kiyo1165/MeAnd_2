from rest_framework.generics import ListAPIView
from accounts.models import User
from .serializers import UserSerializer

class ConsUserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



