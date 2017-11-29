from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restshop.api.user.models import DeliveryInfo, Seller
from restshop.api.user.serializers import UserSerializer, SellerSerializer, DeliveryInfoSerializer, PasswordSerializer
from restshop.api.user.service import DeliveryInfoService


class UserCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['email']
        )

        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(status=status.HTTP_201_CREATED)


class UserView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if bool(request.user.is_anonymous):
            return Response()

        return Response(UserSerializer(request.user).data)


class SellerCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['email']
        )

        staff_group = self.get_staff_group()
        user.groups.add(staff_group)

        user.set_password(serializer.validated_data['password'])
        user.save()

        Seller.objects.create(
            user=user,
            name=serializer.validated_data['seller']['name'],
            address=serializer.validated_data['seller']['address']
        )

        return Response(UserSerializer(user).data)

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
            'property': ('add', 'change'),
            'propertyvalue': ('add', 'change')
        }

        for content_type in content_types:
            for permission in content_types[content_type]:
                codename = '{}_{}'.format(permission, content_type)
                permission = Permission.objects.get(codename=codename)
                group.permissions.add(permission)

        return group


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.data['password'])
        user.save()

        # Need to relogin user, because he is logged out after password change.
        update_session_auth_hash(request, user)

        return Response(status=status.HTTP_200_OK)


class DeliveryInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        try:
            deliveryinfo = user.deliveryinfo
        except DeliveryInfo.DoesNotExist:
            return Response({})

        return Response(DeliveryInfoSerializer(deliveryinfo).data)

    def post(self, request):
        serializer = DeliveryInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        DeliveryInfoService.delete_by_user(request.user)

        serializer.save(user=request.user)

        return Response(status=status.HTTP_201_CREATED)
