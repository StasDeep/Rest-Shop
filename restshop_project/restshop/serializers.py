from rest_framework import serializers

from .models import Product, Unit


class UnitSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('sku', 'price', 'properties')

    def get_properties(self, obj):
        return {property_value.property.name: property_value.value
                for property_value in obj.value_set.all()}


class ProductListSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
        source='tag_set'
    )

    class Meta:
        model = Product
        fields = ('id', 'title', 'tags')


# Inherit from list serializer to get tags field.
class ProductSerializer(ProductListSerializer):
    units = UnitSerializer(
        many=True,
        read_only=True,
        source='unit_set'
    )

    class Meta:
        model = Product
        fields = ('id', 'title', 'tags', 'units')
