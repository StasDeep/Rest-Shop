from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, Order, Unit, OrderUnit
from .serializers import ProductListSerializer, ProductSerializer, UserSerializer, SellerSerializer, OrderSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SellerCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SellerSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data

        user = request.user
        name = data['name']
        address = data['address']
        phone = data['phone']

        order = Order.objects.create(
            user=user,
            name=name,
            address=address,
            phone=phone
        )

        for unit_order in data['units']:
            unit = Unit.objects.get(sku=unit_order['sku'])
            quantity = unit_order['quantity']
            OrderUnit.objects.create(
                order=order,
                unit=unit,
                quantity=quantity
            )

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
