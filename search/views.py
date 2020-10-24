from django.views.generic import TemplateView
from django.db.models import Q
from django.http import JsonResponse

from products.models import Product


class SearchView(TemplateView):
    template_name = 'search/search.html'


def autocomplete_view(request):
    search_query = request.GET.get('search_query')
    autocomplete_products = Product.objects.filter(
        Q(name__icontains=search_query)
    )

    products_json = [
        {
            'name': obj.name,
            'url': obj.get_absolute_url(),
            'is_vegan': obj.is_vegan()
        }
        for obj in autocomplete_products
    ]

    return JsonResponse({'result': products_json})
