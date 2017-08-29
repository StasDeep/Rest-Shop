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
        ordering = ['id']

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ['product__title', '-is_main', 'image']

    def __str__(self):
        return '{}: {}'.format(self.product.title, self.image.name)


class Unit(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    value_set = models.ManyToManyField(to=PropertyValue)
    sku = models.CharField(max_length=255, primary_key=True)
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ['product__title', 'sku']

    def __str__(self):
        properties = ', '.join(str(value) for value in self.value_set.all())
        return '{}: {}'.format(self.product.title, properties)


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
    unit_set = models.ManyToManyField(to=Unit)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=2, choices=STATUSES, default=PENDING)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        items_count = self.unit_set.all().count()
        return 'Order ({} items) by {}'.format(items_count, self.name)
