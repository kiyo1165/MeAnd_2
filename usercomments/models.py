from django.db import models
from accounts.models import User

# Create your models here.
class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField('コメント',max_length=255)
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.comment