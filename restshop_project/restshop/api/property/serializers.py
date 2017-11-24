from rest_framework import serializers

from restshop.api.property.models import Property


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'values': [{
                'id': value.id,
                'value': value.value
            } for value in instance.propertyvalue_set.all()]
        }
