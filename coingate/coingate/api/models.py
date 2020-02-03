from django.db import models


class Transaction(models.Model):
    coin_id = models.IntegerField(blank=True, default=0)
    token = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField(blank=True, null=True)
    value = models.FloatField()
    currency = models.CharField(max_length=5, blank=True)
    order_id = models.CharField(max_length=255, unique=True, blank=True)
    status = models.CharField(max_length=50, blank=True)