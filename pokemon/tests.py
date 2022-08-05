from statistics import mode
from unittest import mock

import requests
from django.test import TestCase

from pokemon import models

# TODO: move those global functions to a factory


def create_types(types_num: int):
    types = []

    for indx, _ in enumerate(range(types_num), 1):
        types.append(
            models.PokemonType(
                name=f'type{indx}',
                url=f'https://type/{indx}',
                slot=1 if indx % 2 == 0 else 2,
            )
        )

    models.PokemonType.objects.bulk_create(types)

    return types


def create_abilities(abilities_num: int):
    abilities = []

    for indx, _ in enumerate(range(abilities_num), 1):
        abilities.append(
            models.PokemonAbility(
                name=f'ability{indx}',
                url=f'https://ability/{indx}',
                is_hidden=False if indx % 2 == 0 else True,
            )
        )

    models.PokemonAbility.objects.bulk_create(abilities)

    return abilities


class MockRequests(object):
    def __init__(self, arg, status_code):
        super(MockRequests, self).__init__()
        self.arg = arg
        self._content = arg
        self.status_code = status_code

    def json(self):
        return self.arg


class PokemonTestCase(TestCase):

    def setUp(self):
        self.created_types = create_types(types_num=3)
        self.created_abilities = create_abilities(abilities_num=3)

    def test_list_pokemons_with_types_and_abilities(self):
        pokemon = models.Pokemon.objects.create(
            pokemon_id=1,
            name='pikachu',
            is_default=True,
            base_experience=125,
            height=25,
            weight=35,
        )

        pokemon.abilities.add(self.created_abilities[0])
        pokemon.types.add(self.created_types[0])

        response = self.client.get('/pokemon/')
        assert response.status_code == 200

        response_data = response.data[0]

        assert response_data['name'] == 'pikachu'
        assert (
            response_data['abilities_list']
            == [{'id': 1, 'name': 'ability1', 'url': 'https://ability/1', 'is_hidden': True}]
        )
        assert (
            response_data['types_list']
            == [{'id': 1, 'name': 'type1', 'url': 'https://type/1', 'slot': 2}]
        )

    def test_list_pokemons_without_types_and_abilities(self):
        models.Pokemon.objects.create(
            pokemon_id=1,
            name='pikachu',
            is_default=True,
            base_experience=125,
            height=25,
            weight=35,
        )

        response = self.client.get('/pokemon/')
        assert response.status_code == 200

        response_data = response.data[0]

        assert response_data['name'] == 'pikachu'
        assert (
            response_data['abilities_list']
            == []
        )
        assert (
            response_data['types_list']
            == []
        )

    @mock.patch('pokemon.serializers.requests.get')
    def test_successful_creation_of_pokemon(self, mock_get):
        response1 = {
            'results': [
                {
                    'name': 'pikapika',
                    'url': 'https://some.url'
                }
            ]
        }
        response2 = {
            'id': 1,
            'name': 'pikapika',
            'is_default': True,
            'base_experience': 100,
            'height': 26,
            'weight': 12,
            'abilities': [
                    {
                        'ability': {
                            'name': 'ab1',
                            'url': 'https:/ability/1',
                        },
                        'is_hidden': False,
                    },
                {
                        'ability': {
                            'name': 'ab2',
                            'url': 'https:/ability/2',
                        },
                        'is_hidden': True,
                    },
            ],
            'types': [
                {
                    'type': {
                        'name': 'typ1',
                        'url': 'https:/type/1',
                    },
                    'slot': 1,
                },
                {
                    'type': {
                        'name': 'typ2',
                        'url': 'https:/type/2',
                    },
                    'slot': 2,
                },
            ],
        }
        fake_responses = [
            MockRequests(response1, 200),
            MockRequests(response2, 200),
        ]

        mock_get.side_effects = fake_responses

        response = self.client.post('/collect_pokemon/')

        assert response.status_code == 200
        assert (
            models.Pokemon.objects.all().values('name')
            == {'name': 'pikapika'}
        )
