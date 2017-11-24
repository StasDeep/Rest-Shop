from django.db import models

from restshop.api.order.models import Order
from restshop.api.unit.models import Unit


class OrderUnit(models.Model):
    PENDING = 'PE'
    REJECTED = 'RE'
    COMPLETED = 'CO'
    STATUSES = (
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed'),
    )

    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    unit = models.ForeignKey(to=Unit)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    status = models.CharField(max_length=2, choices=STATUSES, default=PENDING)

    def __str__(self):
        return '{} pcs of {} by {}'.format(self.quantity, self.unit.product, self.order.name)
