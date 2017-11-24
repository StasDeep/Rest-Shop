from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models

from restshop.api.unit.models import Unit


class CartUnit(models.Model):
    user = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE, related_name='cart_units')
    session = models.ForeignKey(to=Session, null=True, on_delete=models.CASCADE, related_name='cart_units')
    unit = models.ForeignKey(to=Unit)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return '{} unit(s) of {}'.format(self.quantity, self.unit)
