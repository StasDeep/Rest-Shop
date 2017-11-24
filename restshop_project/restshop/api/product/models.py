from django.db import models

from restshop.api.tag.models import Tag
from restshop.api.user.models import Seller


class Product(models.Model):
    tag_set = models.ManyToManyField(to=Tag)
    seller = models.ForeignKey(to=Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
