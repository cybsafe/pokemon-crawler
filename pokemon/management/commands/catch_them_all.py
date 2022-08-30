from typing import TypedDict, Optional
import requests

from django.core.management.base import BaseCommand
from pokemon.models import PokemonMatusCaught


BASE_API_URL = "https://pokeapi.co/api/v2/"


class PokemonDetails(TypedDict):
    name: str
    pokemon_id: int
    description: str
    abilities: Optional[list[str]]


def get_pokemon_description(species_name: str) -> str:
    """
    Get description of the pokemon based on its species name
    """
    url = "{}/pokemon-species/{}/".format(BASE_API_URL, species_name)
    response = requests.get(url).json()  # TODO catch errors
    description = ""
    for flavor_text in response['flavor_text_entries']:
        # Only consider english for now
        if flavor_text['language']['name'] == 'en':
            description += flavor_text['flavor_text']
    return description


def get_pokemon_details(url: str) -> PokemonDetails:
    """
    Get pokemon details from the API based on the pokemon's API url
    """
    response = requests.get(url).json()  # TODO catch errors
    abilities = [a['ability']['name'] for a in response['abilities']]
    description = get_pokemon_description(response['species']['name'])

    return {
        'name': response['name'],
        'pokemon_id': response['id'],  # This is ID from the API, not our ID
        'abilities': abilities or None,
        'description': description,
    }


def update_or_create_pokemon(pokemon_details: PokemonDetails) -> None:
    """
    Based on pokemon_details, determine if the Pokémon is already caught.
    If so, update it, if necessary, otherwise, LET'S CATCH THEM AAAAAALL
    """
    try:
        pokemon = PokemonMatusCaught.objects.get(pokemon_id=pokemon_details['pokemon_id'])
    except PokemonMatusCaught.DoesNotExist:
        # We haven't caught this one yet, lets sort it
        PokemonMatusCaught.objects.create(
            name=pokemon_details['name'],
            pokemon_id=pokemon_details['pokemon_id'],
            abilities=pokemon_details['abilities'],
            description=pokemon_details['description']
        )
    else:
        # Update this bad boy
        save_required = False
        attributes_to_consider = ['name', 'abilities', 'description']
        for attribute in attributes_to_consider:
            if getattr(pokemon, attribute) != pokemon_details[attribute]:
                setattr(pokemon, attribute, pokemon_details[attribute])
                save_required = True

        # Only save if necessary
        if save_required:
            pokemon.save()


class Command(BaseCommand):
    help = 'Catch / update all pokemenons'

    def handle(self, *args, **options):
        """
        Get all pokemons from the API and save* or update them in our database.

        * eeerm, catch them ;)
        """
        next_url = "{}pokemon/".format(BASE_API_URL)
        while next_url:
            response = requests.get(next_url).json()  # TODO catch errors
            next_url = response['next']
            for result in response['results']:
                pokemon_details = get_pokemon_details(result['url'])
                update_or_create_pokemon(pokemon_details)

        pokemon_count = PokemonMatusCaught.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                'We caught them! ({} to be exact) SUCCESS :highfive:'.format(pokemon_count)
            )
        )
