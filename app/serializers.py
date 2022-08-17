from rest_framework import serializers

from app.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer): #serializer to create/update/retrieve our pokemon
    class Meta:
        model = Pokemon
        fields = ['name', 'description', 'attack','special_attack','defense', 'weight', 'move']






