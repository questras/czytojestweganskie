from django.test import TestCase
from django.urls import reverse

import json

from products.models import Ingredient, Product


class SearchViewTests(TestCase):
    def test_search_view_status_code(self):
        r = self.client.get(reverse('search'))
        self.assertEqual(r.status_code, 200)

    def test_search_view_template(self):
        r = self.client.get(reverse('search'))
        self.assertTemplateUsed(r, 'search/search.html')


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

        self.vegan = Product.objects.create(
            name='vegan_product'
        )
        self.vegan.ingredients.add(self.vegan_ingr)

        self.notvegan = Product.objects.create(
            name='notvegan_product'
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
            [json_response['result'][0]['name'], json_response['result'][1]['name']]
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
