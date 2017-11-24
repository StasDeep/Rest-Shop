from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from restshop.api.order_unit.models import OrderUnit
from restshop.api.unit.models import Unit
from restshop.api.unit.serializers import UnitForOrderDetail


class CartUnitSerializer(serializers.Serializer):
    sku = serializers.CharField(write_only=True)
    quantity = serializers.IntegerField(default=1, min_value=1)
    unit = UnitForOrderDetail(read_only=True)

    class Meta:
        model = OrderUnit
        fields = ('sku', 'quantity', 'unit')

    def validate(self, data):
        sku = data['sku']
        quantity = data['quantity']

        try:
            unit = Unit.objects.get(sku=sku)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Unit does not exist')

        if unit.num_in_stock < quantity:
            raise serializers.ValidationError('There are not enough units in stock')

        return data
