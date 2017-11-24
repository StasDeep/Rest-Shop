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
