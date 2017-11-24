from rest_framework import serializers

from restshop.api.order_unit.models import OrderUnit
from restshop.api.unit.serializers import UnitForOrderDetail


class OrderUnitSerializer(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = OrderUnit
        fields = ('quantity', 'status', 'unit')

    def get_unit(self, obj):
        data = UnitForOrderDetail(obj.unit).data

        # Use the price that was at the moment of purchase instead of current price.
        data['price'] = obj.unit_price

        return data

    def get_status(self, obj):
        return obj.get_status_display()

