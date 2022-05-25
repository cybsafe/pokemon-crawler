from pokemon.models import Pokemon
from pokemon.pokemon_api import list_pokemon


from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):


    def handle(self, *args, **kwargs):

        for pokemon_page in list_pokemon():
            for pokemon_data in pokemon_page:
                _id = pokemon_data.get('id')
                del(pokemon_data['id']) 
                Pokemon.objects.update_or_create(id=_id, defaults=pokemon_data)
