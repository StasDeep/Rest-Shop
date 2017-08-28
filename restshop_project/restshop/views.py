from rest_framework import viewsets

from .models import Product
from .serializers import ProductListSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        else:
            return ProductSerializer
