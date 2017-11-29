from django.db import models

from restshop.api.product.models import Product
from restshop.api.property.models import PropertyValue


class Unit(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    value_set = models.ManyToManyField(to=PropertyValue)
    sku = models.CharField(max_length=255, primary_key=True)
    price = models.PositiveIntegerField()
    num_in_stock = models.PositiveIntegerField(default=5)

    class Meta:
        ordering = ['product__title', 'sku']

    def __str__(self):
        properties = ', '.join(str(value) for value in self.value_set.all())
        return '{}: {}'.format(self.product.title, properties)


class UnitImage(models.Model):
    # Units can have same colors, but different sizes.
    # No need to create separate Image instances for these units.
    # That's why ManyToMany is used (one photo can be attached to different units).
    unit_set = models.ManyToManyField(to=Unit, blank=True)
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ['image']

    def __str__(self):
        unit = self.unit_set.first()
        if unit is not None:
            product_title = unit.product.title
        else:
            product_title = 'No unit assigned'

        return '{}: {}'.format(product_title, self.image.name)

    def delete(self, *args, **kwargs):
        self.image.delete()

        super(UnitImage, self).delete(*args, **kwargs)
