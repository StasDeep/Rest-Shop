from django.contrib.auth.models import User
from django.db import models


class Property(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'properties'


class PropertyValue(models.Model):
    value = models.CharField(max_length=255)
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE)

    class Meta:
        ordering = ['property__name', 'value']

    def __str__(self):
        return '{}: {}'.format(self.property.name, self.value)


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Seller(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    tag_set = models.ManyToManyField(to=Tag)
    seller = models.ForeignKey(to=Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


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


class Order(models.Model):
    PENDING = 'PE'
    REJECTED = 'RE'
    COMPLETED = 'CO'
    STATUSES = (
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    unit_set = models.ManyToManyField(to=Unit, through='OrderUnit')
    user = models.ForeignKey(to=User)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=31)
    status = models.CharField(max_length=2, choices=STATUSES, default=PENDING)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        items_count = self.unit_set.all().count()
        return 'Order ({} items) by {}'.format(items_count, self.name)


class OrderUnit(models.Model):
    order = models.ForeignKey(to=Order)
    unit = models.ForeignKey(to=Unit)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return '{} pcs of {} by {}'.format(self.quantity, self.unit.product, self.order.name)
