from django.contrib import admin

from restshop.api.order.models import Order
from restshop.api.order_unit.models import OrderUnit
from restshop.api.product.models import Product
from restshop.api.property.models import PropertyValue, Property
from restshop.api.tag.models import Tag
from restshop.api.unit.models import Unit, UnitImage
from restshop.api.user.models import Seller
from .admin_models import UnitAdmin, ProductAdmin, UnitImageAdmin, OrderAdmin, OrderUnitAdmin, PropertyAdmin, \
    PropertyValueAdmin

admin.site.register([Seller,
                     Tag])

admin.site.register(PropertyValue, PropertyValueAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UnitImage, UnitImageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderUnit, OrderUnitAdmin)
