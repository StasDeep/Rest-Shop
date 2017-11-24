from django.db.models import Max, Min
from rest_framework import serializers

from restshop.api.product.models import Product
from restshop.api.tag.serializers import TagSerializer
from restshop.api.unit.serializers import UnitSerializer


class ProductListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True,
        source='tag_set'
    )
    prices = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'tags', 'prices', 'image')

    def get_prices(self, obj):
        prices = obj.unit_set.aggregate(max=Max('price'), min=Min('price'))
        return {
            'min': prices['min'],
            'max': prices['max']
        }

    def get_image(self, obj):
        unit = obj.unit_set.filter(unitimage__isnull=False).first()

        # If there are no units for the product:
        if unit is None:
            return None

        # Get image (preferably, main one) for the unit.
        image = unit.unitimage_set.order_by('-is_main').first()

        # If there are no images for the unit:
        if image is None:
            return None

        return image.image.url


# Inherit from list serializer to get tags field.
class ProductSerializer(ProductListSerializer):
    units = UnitSerializer(
        many=True,
        read_only=True,
        source='unit_set'
    )

    class Meta:
        model = Product
        fields = ('id', 'title', 'tags', 'description', 'units')
