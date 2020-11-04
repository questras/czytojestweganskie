from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.http import JsonResponse

from products.models import Product


class SearchView(TemplateView):
    template_name = 'search/search.html'


class SearchResultsView(ListView):
    template_name = 'search/search_results.html'
    paginate_by = 10
    context_object_name = 'products'

    def get_queryset(self):
        search_query = self.request.GET.get('search_query') or ''
        return Product.objects.filter(Q(name__icontains=search_query))


def autocomplete_view(request):
    search_query = request.GET.get('search_query')
    autocomplete_products = Product.objects.filter(
        Q(name__icontains=search_query)
    )

    products_json = [
        {
            'name': obj.name,
            'url': obj.get_absolute_url(),
            'image_url': obj.image.url,
            'is_vegan': obj.is_vegan()
        }
        for obj in autocomplete_products
    ]

    return JsonResponse({'result': products_json})
