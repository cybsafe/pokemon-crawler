from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
import requests

from app import settings
from app.models import Pokemon
from app.serializers import PokemonSerializer


def call_pokemon_api(request): #creating the request to call pokemon API
    name = request.data.get("name")
    r = requests.get(url=settings.URL_POKEMON_API + name)
    data = r.json()
    return data, name


class PokemonView(ModelViewSet): #define the main operations for saving the pokemon in our db
    serializer_class = PokemonSerializer

    def get_object(self):
        return Pokemon.objects.get(name=self.kwargs.get("pk"))

    def create(self, request, *args, **kwargs):
        data, name = call_pokemon_api(request)
        Pokemon.objects.create(
            name=name,
            attack=data["stats"][1]["base_stat"],
            special_attack=data["stats"][3]["base_stat"],
            defense=data["stats"][2]["base_stat"],
            weight=data["weight"],
            move=data["moves"][0]["move"]["name"],
        )

        return HttpResponse(status=201)

    def update(self, request, *args, **kwargs):
        data, name = call_pokemon_api(request)

        Pokemon.objects.update_or_create(
            name=name,
            defaults={
                "attack": data["stats"][1]["base_stat"],
                "special_attack": data["stats"][3]["base_stat"],
                "defense": data["stats"][2]["base_stat"],
                "weight": data["weight"],
                "move": data["moves"][0]["move"]["name"],
            },
        )

        return HttpResponse(status=204)
