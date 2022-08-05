from typing import Any

import requests
from rest_framework import serializers

from .models import Pokemon, PokemonAbility, PokemonType


class PokemonSerializer(serializers.ModelSerializer):
    pokemon_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    is_default = serializers.CharField(required=False)
    base_experience = serializers.CharField(required=False)
    height = serializers.CharField(required=False)
    weight = serializers.CharField(required=False)
    abilities_list = serializers.SerializerMethodField(required=False, read_only=True)
    types_list = serializers.SerializerMethodField(required=False, read_only=True)

    def get_abilities_list(self, pokemon: Pokemon):
        return list(pokemon.abilities.all().values())

    def get_types_list(self, pokemon: Pokemon):
        return list(pokemon.types.all().values())

    class Meta:
        model = Pokemon
        fields = (
            'pokemon_id',
            'name',
            'is_default',
            'base_experience',
            'height',
            'weight',
            'types_list',
            'abilities_list',
        )

    def create(self, data: 'dict[str, Any]') -> Pokemon:
        # TODO: instead of pulling all at once
        # pull them in batches
        url = 'https://pokeapi.co/api/v2/pokemon/?offset=0&limit=1200'

        try:
            all_pokemons = requests.get(url).json()['results']
        except Exception as e:  # noqa
            print('Raise error')

        pokemons = []
        # TODO: Iterate over all pokemons and generate all objects accordingly
        for indx, pokemon_data in enumerate(all_pokemons):
            if indx % 100 == 0:
                print(indx)
            pokemon = requests.get(pokemon_data['url']).json()
            types_and_abilities = self.generate_types_and_abilities(
                pokemon,
                should_create=True,
            )

            # TODO: this is not efficient at all
            # look at using async
            pokemon_obj, created = Pokemon.objects.update_or_create(
                pokemon_id=pokemon['id'],
                name=pokemon.get('name', None),
                is_default=pokemon.get('is_default', False),
                base_experience=pokemon.get('base_experience', None),
                height=pokemon.get('height', None),
                weight=pokemon.get('weight', None),
            )

            if created:
                [
                    pokemon_obj.types.add(pokemon_type)
                    for pokemon_type in types_and_abilities['types']
                ]

                [
                    pokemon_obj.abilities.add(pokemon_ability)
                    for pokemon_ability in types_and_abilities['abilities']
                ]

        return pokemon_obj

    def generate_types_and_abilities(
        self,
        pokemon: Pokemon,
        should_create=False,
    ):
        abilities = [
            PokemonAbility(
                name=ability['ability']['name'],
                url=ability['ability']['url'],
                is_hidden=ability['is_hidden']
            ) for ability in pokemon.get('abilities', [])
        ]

        types = [
            PokemonType(
                name=type['type']['name'],
                url=type['type']['url'],
                slot=type['slot']
            ) for type in pokemon.get('types', [])
        ]

        # TODO: the following creates duplicates
        # use update_or_create
        # or extract only the ones that need to be created
        # and bulk create those
        if should_create:
            PokemonAbility.objects.bulk_create(abilities)
            PokemonType.objects.bulk_create(types)

        return {
            'types': types,
            'abilities': abilities,
        }
