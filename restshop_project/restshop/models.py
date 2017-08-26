from django.db import models


class Property(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'properties'


class PropertyValue(models.Model):
    value = models.CharField(max_length=255)
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.property.name, self.value)


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    tag_set = models.ManyToManyField(to=Tag)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


# TODO: install Pillow
# class ProductImage(models.Model):
#     product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="images")


class Unit(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    value_set = models.ManyToManyField(to=PropertyValue)
    sku = models.CharField(max_length=255, primary_key=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        properties = ', '.join(str(value) for value in self.value_set.all())
        return '{}: {}'.format(self.product.title, properties)
