from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import (
    PropertyValue, Property, Product, Tag, Unit
)


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'

    def clean(self):
        values = self.cleaned_data.get('value_set')
        properties = []
        if values:
            for value in values.all():
                if value.property.id not in properties:
                    properties.append(value.property.id)
                else:
                    raise ValidationError('Unit property {} has multiple values'.format(value.property.name))
        return self.cleaned_data


class UnitAdmin(admin.ModelAdmin):
    form = UnitForm

admin.site.register([PropertyValue, Property, Product, Tag, Unit], UnitAdmin)
