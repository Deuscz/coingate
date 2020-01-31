from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField(blank=True, null=True)
    value = models.FloatField()
    purchase_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, blank=True)