from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Seller, Unit, OrderUnit, UnitImage, Product, Order


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


class OrderUnitInline(admin.StackedInline):
    model = OrderUnit
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(OrderUnitInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        seller = get_seller(request)

        if db_field.name == 'unit':
            kwargs['queryset'] = Unit.objects.filter(product__seller=seller).distinct()

        return super(OrderUnitInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class UnitImageInline(admin.TabularInline):
    model = UnitImage.unit_set.through
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(UnitImageInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        seller = get_seller(request)

        if db_field.name == 'unitimage':
            kwargs['queryset'] = UnitImage.objects.filter(unit_set__product__seller=seller).distinct()

        return super(UnitImageInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class StaffModelAdmin(admin.ModelAdmin):
    seller_field_path = 'seller'

    def get_queryset(self, request):
        queryset = super(StaffModelAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return queryset

        seller = get_seller(request)

        kwargs = {self.seller_field_path: seller}

        # Add distinct to remove duplicates when searching through M2M.
        return queryset.filter(**kwargs).distinct()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(StaffModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        seller = get_seller(request)

        if db_field.name == 'product':
            kwargs['queryset'] = Product.objects.filter(seller=seller)

        if db_field.name == 'unit':
            kwargs['queryset'] = Unit.objects.filter(product__seller=seller).distinct()

        if db_field.name == 'order':
            kwargs['queryset'] = Order.objects.filter(unit_set__product__seller=seller).distinct()

        return super(StaffModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(StaffModelAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

        seller = get_seller(request)

        if db_field.name == 'unit_set':
            kwargs['queryset'] = Unit.objects.filter(product__seller=seller)

        return super(StaffModelAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class ProductAdmin(StaffModelAdmin):
    seller_field_path = 'seller'


class UnitAdmin(StaffModelAdmin):
    form = UnitForm
    seller_field_path = 'product__seller'
    inlines = (UnitImageInline,)


class UnitImageAdmin(StaffModelAdmin):
    seller_field_path = 'unit_set__product__seller'


class OrderAdmin(StaffModelAdmin):
    seller_field_path = 'unit_set__product__seller'
    inlines = (OrderUnitInline,)


class OrderUnitAdmin(StaffModelAdmin):
    seller_field_path = 'unit__product__seller'
