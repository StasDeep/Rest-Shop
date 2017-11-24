from rest_framework import serializers

from restshop.api.unit.models import Unit


class UnitSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('sku', 'price', 'properties', 'images', 'num_in_stock')

    def get_properties(self, obj):
        return [{
                    'name': property_value.property.name,
                    'value': property_value.value
                } for property_value in obj.value_set.all()]

    def get_images(self, obj):
        images = obj.unitimage_set.all()

        if images.exists():
            return [image.image.url for image in images.all()]
        else:
            return []


class UnitForOrderDetail(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title')
    properties = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(source='product.id')

    class Meta:
        model = Unit
        fields = ('title', 'properties', 'image', 'product_id', 'price', 'sku', 'num_in_stock')

    def get_properties(self, obj):
        return [{
            'name': property_value.property.name,
            'value': property_value.value
        } for property_value in obj.value_set.all()]

    def get_image(self, obj):
        image = obj.unitimage_set.order_by('-is_main').first()

        if image is None:
            return None

        return image.image.url
