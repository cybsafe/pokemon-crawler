import asyncio

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand

from pokemon.models import Pokemon
from pokemon.pokemon_api import list_pokemon


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        async def get_pokemon_list():
            pokemon_list = list_pokemon()
            async for pokemon_page in pokemon_list:
                for pokemon_data in pokemon_page:
                    _id = pokemon_data.get('id')
                    del(pokemon_data['id'])

                await sync_to_async(Pokemon.objects.update_or_create)(id=_id, defaults=pokemon_data)

        asyncio.run(get_pokemon_list())
