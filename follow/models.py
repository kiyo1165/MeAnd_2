from django.db import models
from django.utils import timezone
from accounts.models import User
# Create your models here.
class Follow(models.Model):
    follow_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_user')
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='follower_user')
    created_at = models.DateTimeField(default=timezone.now)