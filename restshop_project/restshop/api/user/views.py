from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restshop.api.user.models import DeliveryInfo
from restshop.api.user.serializers import UserSerializer, SellerSerializer, DeliveryInfoSerializer


class UserCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if bool(request.user.is_anonymous):
            return Response()

        return Response(UserSerializer(request.user).data)


class SellerCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SellerSerializer


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        user.set_password(request.data['password'])
        user.save()

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

        # Remove current delivery info if exists.
        try:
            request.user.deliveryinfo.delete()
        except DeliveryInfo.DoesNotExist:
            pass

        serializer.save(user=request.user)

        return Response(status=status.HTTP_201_CREATED)
