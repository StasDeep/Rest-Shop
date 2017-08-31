from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Seller, Unit


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

    def clean(self):
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
        return self.cleaned_data


class StaffModelAdmin(admin.ModelAdmin):
    seller_field_path = 'seller'

    def get_queryset(self, request):
        queryset = super(StaffModelAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return queryset

        seller = Seller.objects.get(user=request.user)

        kwargs = {self.seller_field_path: seller}

        # Add distinct to remove duplicates when searching through M2M.
        return queryset.filter(**kwargs).distinct()


class ProductAdmin(StaffModelAdmin):
    seller_field_path = 'seller'


class UnitAdmin(StaffModelAdmin):
    form = UnitForm
    seller_field_path = 'product__seller'


class UnitImageAdmin(StaffModelAdmin):
    seller_field_path = 'unit_set__product__seller'


class OrderAdmin(StaffModelAdmin):
    seller_field_path = 'unit_set__product__seller'
