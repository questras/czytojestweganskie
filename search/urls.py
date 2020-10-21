from django.urls import path

from .views import SearchView, autocomplete_view

urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('autocomplete/', autocomplete_view, name='autocomplete'),
]