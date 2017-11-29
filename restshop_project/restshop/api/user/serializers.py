from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from restshop.api.user.models import DeliveryInfo


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6,
                'max_length': 127
            },
            'email': {
                'validators': [UniqueValidator(queryset=User.objects.all())]
            }
        }


class SellerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='seller.name')
    address = serializers.CharField(source='seller.address')

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'address')


class DeliveryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryInfo
        fields = ('name', 'address', 'phone')


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=127)
