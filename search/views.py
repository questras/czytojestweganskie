from django.views.generic import ListView
from django.db.models import Q
from django.http import JsonResponse

from products.models import Product


class SearchView(ListView):
    template_name = 'search/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


def autocomplete(request):
    search_query = request.GET.get('search')
    print(f'q:{search_query}')
    print(type(search_query))
    autocomplete_products = Product.objects.filter(
        Q(name__icontains=search_query)
    )

    json_products = [
        {
            'name': obj.name,
            'url': obj.get_absolute_url(),
            'is_vegan': obj.is_vegan()
        }
        for obj in autocomplete_products
    ]

    return JsonResponse({'result': json_products})
