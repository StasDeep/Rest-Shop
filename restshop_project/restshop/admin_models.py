from django import forms
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.core.exceptions import ValidationError

from restshop.api.order.models import Order
from restshop.api.order_unit.models import OrderUnit
from restshop.api.product.models import Product
from restshop.api.unit.models import Unit, UnitImage
from restshop.api.user.models import Seller

SELLER_LOOKUPS = {
    'unit': {
        'lookup': 'product__seller',
        'model': Unit
    },
    'unit_set': {
        'lookup': 'product__seller',
        'model': Unit
    },
    'unitimage': {
        'lookup': 'unit_set__product__seller',
        'model': UnitImage
    },
    'product': {
        'lookup': 'seller',
        'model': Product
    },
    'order': {
        'lookup': 'unit_set__product__seller',
        'model': Order
    },
    'orderunit': {
        'lookup': 'unit__product__seller',
        'model': OrderUnit
    },
}


def get_seller(request):
    return Seller.objects.get(user=request.user)


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

    def clean_value_set(self):
        values = self.cleaned_data.get('value_set')

        # Multiple values for one property (Color: Black, Color: White)
        # are disallowed for a single unit.
        properties = []
        if values:
            for value in values.all():
                if value.property.id not in properties:
                    properties.append(value.property.id)
                else:
                    # Make an exclusion for Color, because a unit can have multiple.
                    if value.property.name != 'Color':
                        raise ValidationError(
                            'Unit property {} has multiple values'.format(value.property.name)
                        )
        return values


class QuerysetForSellerMixin(BaseModelAdmin):
    """Add restrictions to querysets which are displayed to sellers in foreignkey and manytomany fields."""

    def set_filtered_queryset(self, db_field, request, kwargs):
        """Change kwargs['queryset'] to show records related only to seller who requests them."""
        seller = get_seller(request)

        for field in SELLER_LOOKUPS:
            if db_field.name == field:
                model = SELLER_LOOKUPS[field]['model']
                lookup_kwargs = {SELLER_LOOKUPS[field]['lookup']: seller}
                kwargs['queryset'] = model.objects.filter(**lookup_kwargs).distinct()

        if db_field.name == 'seller':
            kwargs['queryset'] = Seller.objects.filter(id=seller.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            self.set_filtered_queryset(db_field, request, kwargs)

        return super(QuerysetForSellerMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            self.set_filtered_queryset(db_field, request, kwargs)

        return super(QuerysetForSellerMixin, self).formfield_for_manytomany(db_field, request, **kwargs)


class OrderUnitInline(QuerysetForSellerMixin, admin.StackedInline):
    model = OrderUnit
    extra = 1
    can_delete = False

    def get_max_num(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super(OrderUnitInline, self).get_max_num(request, obj, **kwargs)

        # If not superuser, forbid adding units to order.
        return 0

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields

        return self.readonly_fields + ('unit', 'quantity', 'unit_price')


class UnitImageInline(QuerysetForSellerMixin, admin.StackedInline):
    model = UnitImage.unit_set.through
    extra = 1


class StaffModelAdmin(QuerysetForSellerMixin, admin.ModelAdmin):
    """Add restrictions to queryset which are displayed to sellers."""
    seller_field_path = 'seller'

    def get_queryset(self, request):
        queryset = super(StaffModelAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return queryset

        seller = get_seller(request)

        lookup_kwargs = {self.seller_field_path: seller}

        # Add distinct to remove duplicates when searching through M2M.
        return queryset.filter(**lookup_kwargs).distinct()


class ProductAdmin(StaffModelAdmin):
    seller_field_path = SELLER_LOOKUPS['product']['lookup']

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return super(ProductAdmin, self).get_exclude(request, obj)

        return ['seller']

    def save_model(self, request, product, form, change):
        # If seller is creating product, set seller field.
        if not request.user.is_superuser:
            product.seller = get_seller(request)

        super(ProductAdmin, self).save_model(request, product, form, change)


class UnitAdmin(StaffModelAdmin):
    seller_field_path = SELLER_LOOKUPS['unit']['lookup']
    form = UnitForm
    # inlines = (UnitImageInline,)
    raw_id_fields = ('product', 'value_set')


class UnitImageAdmin(StaffModelAdmin):
    seller_field_path = SELLER_LOOKUPS['unitimage']['lookup']
    raw_id_fields = ('unit_set',)


class OrderAdmin(StaffModelAdmin):
    seller_field_path = SELLER_LOOKUPS['order']['lookup']
    inlines = (OrderUnitInline,)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields

        return self.readonly_fields + ('user', 'name', 'address', 'phone')


class OrderUnitAdmin(StaffModelAdmin):
    seller_field_path = SELLER_LOOKUPS['orderunit']['lookup']
    raw_id_fields = ('unit', 'order')


class PropertyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields

        return self.readonly_fields + ('name',)


class PropertyValueAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields

        return self.readonly_fields + ('property', 'value')
