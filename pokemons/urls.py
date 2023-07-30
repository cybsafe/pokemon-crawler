from django.urls import path
from .views import GetAllPokemonsView, PokemonDataUpdateView


from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "get-all-pokemons/", views.GetAllPokemonsView.as_view(), name="get-all-pokemons"
    ),
    path(
        "update-pokemon-data/",
        PokemonDataUpdateView.as_view(),
        name="update-pokemon-data",
    ),
    path(
        "pokemon/<str:pokemon_name>/",
        views.PokemonDetailsView.as_view(),
        name="pokemon-details",
    ),
]
