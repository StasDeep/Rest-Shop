from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from restshop.api.user.models import Seller, DeliveryInfo


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'validators': [UniqueValidator(queryset=User.objects.all())]
            }
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class SellerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='seller.name')
    address = serializers.CharField(source='seller.address')

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'address')

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email']
        )

        staff_group = self.get_staff_group()
        user.groups.add(staff_group)

        user.set_password(validated_data['password'])
        user.save()

        Seller.objects.create(
            user=user,
            name=validated_data['seller']['name'],
            address=validated_data['seller']['address']
        )

        return user

    def get_staff_group(self):
        """Get staff group with seller permissions or create if does not exist."""
        try:
            return Group.objects.get(name='Staff')
        except ObjectDoesNotExist:
            group = Group.objects.create(name='Staff')

        all_permissions = ('add', 'change', 'delete')
        content_types = {
            'unit': all_permissions,
            'product': all_permissions,
            'unitimage': all_permissions,
            'orderunit': all_permissions,
            'order': ('change',),
            'property': ('add',),
            'propertyvalue': ('add',)
        }

        for content_type in content_types:
            for permission in content_types[content_type]:
                codename = '{}_{}'.format(permission, content_type)
                permission = Permission.objects.get(codename=codename)
                group.permissions.add(permission)

        return group


class DeliveryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryInfo
        fields = ('name', 'address', 'phone')
