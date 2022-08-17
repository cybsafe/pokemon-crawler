from django.core.management import call_command
from django.test import TestCase
from app.models import Pokemon
from app.serializers import PokemonSerializer


def getPayload(**kwargs): #creating payload
    return {
        "id": 1,
        "name": "unittesting",
        "attack": 1,
        "special_attack": 1,
        "defense": 1,
        "weight": 1,
        "move": "test",
        **kwargs,
    }


class TestCreateCollection(TestCase):
    def setUp(self):
        super().setUp()

        call_command("loaddata", "app/test/fixtures/add_pokemon.json", verbosity=0)
        self.pokemon_name = "unittesting"
        self.response_payload = getPayload()

    def test_serializer(self):
        pokemon = Pokemon.objects.get(name=self.pokemon_name)

        serializer_class = PokemonSerializer(pokemon, data=self.response_payload)
        self.assertTrue(serializer_class.is_valid(raise_exception=True))
        self.assertEqual(pokemon.__dict__.get("id"), self.response_payload.get("id"))

    def test_serializer_with_wrong_data(self):
        pokemon = Pokemon.objects.get(name=self.pokemon_name)

        serializer_class = PokemonSerializer(pokemon, data=getPayload(**{"name": None}))
        with self.assertRaises(Exception):
            self.assertRaises(serializer_class.is_valid(raise_exception=True))
