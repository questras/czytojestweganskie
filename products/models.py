import uuid

from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    vegan = models.BooleanField()

    def __str__(self):
        string = self.name
        string += '(vegan)' if self.vegan else '(not vegan)'

        return string


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    ingredients = models.ManyToManyField(Ingredient, related_name='products')

    def is_vegan(self):
        return len(self.ingredients.filter(vegan=False)) == 0

    def __str__(self):
        string = self.name
        string += '(vegan)' if self.is_vegan() else '(not vegan)'

        return string

    def get_absolute_url(self):
        return reverse('product_detail', args=(self.id,))
