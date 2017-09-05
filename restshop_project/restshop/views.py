from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Product, Order, Unit, OrderUnit, PropertyValue, Tag, Property
from .serializers import ProductListSerializer, ProductSerializer, UserSerializer, SellerSerializer, \
    OrderUnitSerializer, OrderListSerializer, OrderDetailSerializer, TagSerializer, PropertySerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'has_prev': self.page.has_previous(),
            'has_next': self.page.has_next(),
            'results': data
        })


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Product.objects.all()

        q = self.request.query_params.get('q', None)
        tags = self.request.GET.getlist('tags')
        criteria = self.request.GET.getlist('properties')
        in_stock = self.request.query_params.get('in_stock', None)
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)

        if q is not None:
            queryset = queryset.filter(title__icontains=q)

        if tags:
            for tag in tags:
                queryset = queryset.filter(tag_set__name__iexact=tag).distinct()

        if criteria:
            for criterium in criteria:
                queryset = queryset.filter(unit__value_set__in=[criterium]).distinct()

        if in_stock == '1':
            queryset = queryset.filter(unit__num_in_stock__gt=0).distinct()

        if price_min is not None:
            queryset = queryset.filter(unit__price__gte=int(price_min)).distinct()

        if price_max is not None:
            queryset = queryset.filter(unit__price__lte=int(price_max)).distinct()

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SellerCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SellerSerializer


class OrderViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        user = request.user
        queryset = Order.objects.filter(user=user)
        serializer = OrderListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = request.user
        order = Order.objects.get(pk=pk)

        if user.id != order.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = OrderDetailSerializer(order)
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

            if unit.num_in_stock >= quantity:
                OrderUnit.objects.create(
                    order=get_order_by_seller(unit_seller),
                    unit=unit,
                    quantity=quantity
                )
                unit.num_in_stock -= quantity
                unit.save()

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
