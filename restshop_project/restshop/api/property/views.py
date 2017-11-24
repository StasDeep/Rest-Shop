from rest_framework import generics

from restshop.api.property.models import Property
from restshop.api.property.serializers import PropertySerializer


class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
