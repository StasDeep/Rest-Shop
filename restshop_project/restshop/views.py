from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Product, Order, Unit, OrderUnit
from .serializers import ProductListSerializer, ProductSerializer, UserSerializer, SellerSerializer, \
    OrderUnitSerializer, OrderListSerializer


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


class OrderViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        user = request.user
        queryset = Order.objects.filter(user=user)
        serializer = OrderListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderUnitSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data

        user = request.user
        name = data['name']
        address = data['address']
        phone = data['phone']

        # One order is broken into several ones: one for each seller.
        # It's done to prevent ambiguous statuses.
        # While iterating through units,
        # their sellers are pushed to sellers list
        # and corresponding orders are pushed to orders list by the same index.
        sellers = []
        orders = []

        def get_order_by_seller(seller):
            if seller in sellers:
                order_index = sellers.index(seller)
                return orders[order_index]
            else:
                order = Order.objects.create(
                    user=user,
                    name=name,
                    address=address,
                    phone=phone
                )

                sellers.append(seller)
                orders.append(order)

                return order

        for unit_order in data['units']:
            unit = Unit.objects.get(sku=unit_order['sku'])
            unit_seller = unit.product.seller
            quantity = unit_order['quantity']
            OrderUnit.objects.create(
                order=get_order_by_seller(unit_seller),
                unit=unit,
                quantity=quantity
            )

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
