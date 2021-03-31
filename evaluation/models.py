from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User
# Create your models here.
class Evaluation(models.Model):
    number = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], blank=True)
    comment = models.TextField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)