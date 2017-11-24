from collections import defaultdict

from django.db.models import Max, Min
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from restshop.api.product.models import Product
from restshop.api.product.serializers import ProductListSerializer, ProductSerializer
from restshop.api.property.models import PropertyValue
from restshop.api.unit.models import Unit


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
