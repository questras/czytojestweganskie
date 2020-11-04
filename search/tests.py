from tempfile import NamedTemporaryFile

from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.images import ImageFile

import json

from products.models import Ingredient, Product


def get_temporary_image_file():
    """Return temporary image file for testing purposes. This file
    is deleted after the test using it is finished. File's url is in
    file.name attribute.
    """
    img_dir = settings.MEDIA_ROOT
    return ImageFile(NamedTemporaryFile(dir=img_dir, suffix='.jpg'))


class SearchViewTests(TestCase):
    def test_search_view_status_code(self):
        r = self.client.get(reverse('search'))
        self.assertEqual(r.status_code, 200)

    def test_search_view_template(self):
        r = self.client.get(reverse('search'))
        self.assertTemplateUsed(r, 'search/search.html')


class SearchViewResultsTests(TestCase):
    def test_status_code(self):
        r = self.client.get(reverse('search_results'))
        self.assertEqual(r.status_code, 200)
        r = self.client.get(reverse('search_results'),
                            data={'search_query': 'test'})
        self.assertEqual(r.status_code, 200)

    def test_correct_template(self):
        r = self.client.get(reverse('search_results'))
        self.assertTemplateUsed(r, 'search/search_results.html')

    def test_correct_results(self):
        tmp_image = get_temporary_image_file()
        product1 = Product.objects.create(
            name='test',
            image=tmp_image.name
        )
        product2 = Product.objects.create(
            name='testproduct',
            image=tmp_image.name
        )

        # Gets all products when no search_query.
        r = self.client.get(reverse('search_results'))
        self.assertContains(r, 'test')
        self.assertContains(r, 'testproduct')
        self.assertIn(product1, r.context['products'])
        self.assertIn(product2, r.context['products'])

        # Gets both products.
        r = self.client.get(reverse('search_results'),
                            data={'search_query': 'test'})
        self.assertContains(r, 'test')
        self.assertContains(r, 'testproduct')
        self.assertIn(product1, r.context['products'])
        self.assertIn(product2, r.context['products'])

        # Gets only product2.
        r = self.client.get(reverse('search_results'),
                            data={'search_query': 'product'})
        self.assertContains(r, 'testproduct')
        self.assertNotIn(product1, r.context['products'])
        self.assertIn(product2, r.context['products'])

        # Gets no products.
        r = self.client.get(reverse('search_results'),
                            data={'search_query': 'noresult'})
        self.assertNotIn(product1, r.context['products'])
        self.assertNotIn(product2, r.context['products'])


class AutocompleteViewTests(TestCase):
    def setUp(self) -> None:
        self.vegan_ingr = Ingredient.objects.create(
            name='ingredient1',
            vegan=True
        )
        self.notvegan_ingr = Ingredient.objects.create(
            name='ingredient2',
            vegan=False
        )

        tmp_image = get_temporary_image_file()
        self.vegan = Product.objects.create(
            name='vegan_product',
            image=tmp_image.name
        )
        self.vegan.ingredients.add(self.vegan_ingr)

        self.notvegan = Product.objects.create(
            name='notvegan_product',
            image=tmp_image.name
        )
        self.notvegan.ingredients.add(self.notvegan_ingr)

    def test_correct_response(self):
        r = self.client.get(
            reverse('autocomplete'),
            data={'search_query': 'notvegan'}
        )
        json_response = json.loads(r.content)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json_response['result']), 1)
        self.assertEqual(json_response['result'][0]['name'], self.notvegan.name)

        r = self.client.get(
            reverse('autocomplete'),
            data={'search_query': 'vegan'}
        )
        json_response = json.loads(r.content)

        self.assertEqual(len(json_response['result']), 2)

        # In sorted order, response_items_names should be:
        # ['notvegan_product', 'vegan_product']
        response_items_names = sorted(
            [json_response['result'][0]['name'],
             json_response['result'][1]['name']]
        )
        self.assertEqual(self.notvegan.name, response_items_names[0])
        self.assertEqual(self.vegan.name, response_items_names[1])

    def test_correct_autocomplete_item_response_content(self):
        r = self.client.get(
            reverse('autocomplete'),
            data={'search_query': 'notvegan'}
        )
        autocomplete_item = json.loads(r.content)['result'][0]

        self.assertEqual(autocomplete_item['name'], self.notvegan.name)
        self.assertEqual(
            autocomplete_item['url'], self.notvegan.get_absolute_url())
        self.assertEqual(
            autocomplete_item['is_vegan'], self.notvegan.is_vegan())
