from django import forms
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.core.exceptions import ValidationError

from .models import Seller, Unit, OrderUnit, UnitImage, Product, Order


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


class UnitAdmin(StaffModelAdmin):
    seller_field_path = SELLER_LOOKUPS['unit']['lookup']
    form = UnitForm
    inlines = (UnitImageInline,)


class UnitImageAdmin(StaffModelAdmin):
    seller_field_path = SELLER_LOOKUPS['unitimage']['lookup']


class OrderAdmin(StaffModelAdmin):
    seller_field_path = SELLER_LOOKUPS['order']['lookup']
    inlines = (OrderUnitInline,)


class OrderUnitAdmin(StaffModelAdmin):
    seller_field_path = SELLER_LOOKUPS['orderunit']['lookup']
