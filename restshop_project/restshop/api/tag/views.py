from rest_framework import generics

from restshop.api.tag.models import Tag
from restshop.api.tag.serializers import TagSerializer


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
