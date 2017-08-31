from django.contrib import admin

from .models import (
    Order,
    OrderUnit,
    PropertyValue,
    Property,
    Product,
    Seller,
    Tag,
    Unit,
    UnitImage
)
from .admin_models import UnitAdmin, ProductAdmin, UnitImageAdmin, OrderAdmin


admin.site.register([OrderUnit,
                     PropertyValue,
                     Property,
                     Seller,
                     Tag])

admin.site.register(Unit, UnitAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UnitImage, UnitImageAdmin)
admin.site.register(Order, OrderAdmin)
