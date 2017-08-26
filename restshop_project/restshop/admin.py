from django.contrib import admin

from .models import (
    PropertyValue, Property, Product, Tag, Unit
)

# Register your models here.
admin.site.register((PropertyValue, Property, Product, Tag, Unit))
