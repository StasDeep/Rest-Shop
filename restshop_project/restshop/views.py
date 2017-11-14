from collections import defaultdict

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models import Min, Max
from rest_framework import generics, status, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import Product, Order, Unit, OrderUnit, PropertyValue, Tag, Property, CartUnit
from .serializers import ProductListSerializer, ProductSerializer, UserSerializer, SellerSerializer, \
    OrderListSerializer, OrderDetailSerializer, TagSerializer, PropertySerializer, CartUnitSerializer, \
    OrderSerializer


class ProductSetPagination(PageNumberPagination):
    page_size = 32

    def get_paginated_response(self, data):
        prices = Unit.objects.aggregate(max=Max('price'), min=Min('price'))
        return Response({
            'meta': {
                'page': self.page.number,
                'has_prev': self.page.has_previous(),
                'has_next': self.page.has_next(),
                'min_price': prices['min'],
                'max_price': prices['max'],
            },
            'data': data
        })


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductSetPagination

    def get_queryset(self):
        queryset = Product.objects.all()

        q = self.request.query_params.get('q', None)
        tags = self.request.query_params.get('tags')
        criteria = self.request.query_params.get('properties')
        in_stock = self.request.query_params.get('in_stock', None)
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)

        if q is not None:
            queryset = queryset.filter(title__icontains=q)

        if tags:
            tags = tags.split(',')

            for tag in tags:
                queryset = queryset.filter(tag_set__name__iexact=tag).distinct()

        if criteria:
            criteria = criteria.split(',')
            values = PropertyValue.objects.filter(id__in=criteria)

            grouped_values = defaultdict(list)
            for value in values:
                grouped_values[value.property_id].append(value.id)

            for key in grouped_values:
                values = grouped_values[key]
                queryset = queryset.filter(unit__value_set__in=values).distinct()

        if in_stock == '1':
            queryset = queryset.filter(unit__num_in_stock__gt=0).distinct()

        if price_min is not None and price_min.isdigit():
            queryset = queryset.filter(unit__price__gte=int(price_min)).distinct()

        if price_max is not None and price_max.isdigit():
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
    permission_classes = (AllowAny,)

    def list(self, request):
        user = request.user

        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        if not bool(request.user.is_anonymous):
            cart_units = request.user.cart_units.all()
            data['user'] = request.user
        else:
            if request.session.session_key is None:
                request.session.save()

            cart_units = Session.objects.get(session_key=request.session.session_key).cart_units.all()
            data['user'] = None

        if cart_units.count() == 0:
            raise serializers.ValidationError('Cart is empty, nothing to order')

        order = Order.objects.create(**data)

        for cart_unit in cart_units:
            if cart_unit.unit.num_in_stock < cart_unit.quantity:
                raise serializers.ValidationError(
                    'Not enough units in stock: {}'.format(cart_unit.unit.sku)
                )

        for cart_unit in cart_units:
            unit = cart_unit.unit

            OrderUnit.objects.create(
                order=order,
                quantity=cart_unit.quantity,
                unit=unit,
                unit_price=unit.price
            )

            unit.num_in_stock -= cart_unit.quantity
            unit.save()

            # Clear cart
            cart_unit.delete()

        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)


class CartView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if not bool(request.user.is_anonymous):
            cart_units = request.user.cart_units.all()
        else:
            if request.session.session_key is None:
                request.session.save()

            cart_units = Session.objects.get(session_key=request.session.session_key).cart_units.all()

        return Response(CartUnitSerializer(cart_units, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartUnitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        unit = Unit.objects.get(sku=data['sku'])

        cart_unit_data = {
            'unit': unit,
            'user': None,
            'session': None
        }

        if not bool(request.user.is_anonymous):
            cart_unit_data['user'] = request.user
        else:
            if request.session.session_key is None:
                request.session.save()

            cart_unit_data['session'] = Session.objects.get(session_key=request.session.session_key)

        cart_unit = CartUnit.objects.filter(**cart_unit_data).first()

        if cart_unit is None:
            cart_unit = CartUnit(**cart_unit_data)

        cart_unit.quantity = data['quantity']
        cart_unit.save()

        return Response(status=status.HTTP_201_CREATED)


class UserView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if bool(request.user.is_anonymous):
            return Response()

        return Response(UserSerializer(request.user).data)
