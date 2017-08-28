from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Product, Unit


EMPTY_PHOTO_URL = 'product_images/empty.jpg'


class UnitSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('sku', 'price', 'properties')

    def get_properties(self, obj):
        return [{
                    'name': property_value.property.name,
                    'value': property_value.value
                } for property_value in obj.value_set.all()]


class ProductListSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
        source='tag_set'
    )

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'tags', 'image')

    def get_image(self, obj):
        try:
            return obj.productimage_set.get(is_main=True).image.url
        except ObjectDoesNotExist:
            return EMPTY_PHOTO_URL


# Inherit from list serializer to get tags field.
class ProductSerializer(ProductListSerializer):
    units = UnitSerializer(
        many=True,
        read_only=True,
        source='unit_set'
    )

    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'tags', 'units', 'images')

    def get_images(self, obj):
        images = obj.productimage_set.all()

        if images.exists():
            return [image.image.url for image in images.all()]
        else:
            return [EMPTY_PHOTO_URL]
