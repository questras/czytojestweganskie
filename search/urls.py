from django.urls import path

from .views import SearchView, autocomplete

urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('autocomplete_search/', autocomplete, name='autocomplete'),
]