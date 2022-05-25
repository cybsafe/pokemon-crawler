from django.shortcuts import render
from pokemon.models import Pokemon
from pokemon.serializers import PokemonSerializer
from rest_framework import viewsets

# Create your views here.

class PokemonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

