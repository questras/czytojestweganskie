from django.test import TestCase
from django.urls import reverse

from .models import Product, Ingredient


class IngredientTests(TestCase):
    def setUp(self) -> None:
        self.vegan = Ingredient.objects.create(
            name='ingredient1',
            vegan=True
        )
        self.notvegan = Ingredient.objects.create(
            name='ingredient2',
            vegan=False
        )

    def test_ingredient_object(self):
        self.assertEqual(self.vegan.name, 'ingredient1')
        self.assertEqual(self.vegan.vegan, True)

        self.assertEqual(self.notvegan.name, 'ingredient2')
        self.assertEqual(self.notvegan.vegan, False)

    def test_str_method(self):
        self.assertEqual(str(self.vegan), 'ingredient1(vegan)')
        self.assertEqual(str(self.notvegan), 'ingredient2(not vegan)')


class ProductTests(TestCase):
    def setUp(self) -> None:
        self.vegan_ingr = Ingredient.objects.create(
            name='ingredient1',
            vegan=True
        )
        self.notvegan_ingr = Ingredient.objects.create(
            name='ingredient2',
            vegan=False
        )

        self.vegan = Product.objects.create(
            name='product1'
        )
        self.vegan.ingredients.add(self.vegan_ingr)

        self.notvegan = Product.objects.create(
            name='product2'
        )
        self.notvegan.ingredients.add(self.notvegan_ingr)

    def test_product_object(self):
        self.assertEqual(self.vegan.name, 'product1')
        self.assertEqual(self.notvegan.name, 'product2')

    def test_is_vegan(self):
        self.assertEqual(self.vegan.is_vegan(), True)
        self.assertEqual(self.notvegan.is_vegan(), False)

    def test_str_method(self):
        self.assertEqual(str(self.vegan), 'product1(vegan)')
        self.assertEqual(str(self.notvegan), 'product2(not vegan)')

    def test_get_absolute_url(self):
        self.assertEqual(self.vegan.get_absolute_url(),
                         reverse('product_detail', args=(self.vegan.id,)))
        self.assertEqual(self.notvegan.get_absolute_url(),
                         reverse('product_detail', args=(self.notvegan.id,)))

    def test_detail_view_status_code(self):
        r = self.client.get(self.vegan.get_absolute_url())
        self.assertEqual(r.status_code, 200)

    def test_detail_view_template(self):
        r = self.client.get(self.vegan.get_absolute_url())
        self.assertTemplateUsed('products/product_detail.html')
        self.assertContains(r, 'Vegan!')
        self.assertContains(r, 'product1')
        self.assertContains(r, 'ingredient1')

        r = self.client.get(self.notvegan.get_absolute_url())
        self.assertTemplateUsed('products/product_detail.html')
        self.assertContains(r, 'Not vegan!')
        self.assertContains(r, 'product2')
        self.assertContains(r, 'ingredient2')
