from rest_framework import serializers

from restshop.api.order.models import Order
from restshop.api.order_unit.serializers import OrderUnitSerializer


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('name', 'address', 'phone')


class OrderListSerializer(serializers.ModelSerializer):
    units_num = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'units_num')

    def get_units_num(self, obj):
        return obj.unit_set.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    units = OrderUnitSerializer(
        many=True,
        read_only=True,
        source='orderunit_set'
    )

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'name', 'address', 'phone', 'units')
