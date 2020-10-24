from django.urls import path

from .views import SearchView, SearchResultsView, autocomplete_view

urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('results/', SearchResultsView.as_view(), name='search_results'),
    path('autocomplete/', autocomplete_view, name='autocomplete'),
]
