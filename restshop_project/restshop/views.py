from django.contrib.auth.models import User
from rest_framework import generics

from .models import Product
from .serializers import ProductListSerializer, ProductSerializer, UserSerializer, SellerSerializer


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
