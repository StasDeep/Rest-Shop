from django.contrib.auth.models import User
from django.db import models


class Seller(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DeliveryInfo(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=31)
