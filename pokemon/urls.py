from django.conf.urls import url

from .views import ListPokemonView, RemovePokemonView

urlpatterns = [
    url(r'^$', ListPokemonView.as_view(), name="list-pokemon"),
    url(r'^collect_pokemon$', ListPokemonView.as_view(), name="pokemon-collect"),
    url(r'^remove_pokemon$', RemovePokemonView.as_view(), name="pokemon-remove"),
]
