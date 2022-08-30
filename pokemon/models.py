from django.contrib.postgres.fields import ArrayField
from django.db import models


class PokemonMatusCaught(models.Model):  # personal touch :seenoevil:
    # Due to time constraints, lets capture only the following information
    # Store pokemon_id separately to our primary key id. This is to
    # make it explicit that pokemons have an "external id"
    pokemon_id = models.IntegerField(
        unique=True, db_index=True, help_text="External Pokemon ID"
    )
    name = models.CharField(max_length=128)
    description = models.TextField()
    # Store abilities, just a simple array of them.
    # TODO create a separate Abilities model and store more details
    abilities = ArrayField(models.CharField(max_length=128), null=True)

    class Meta:
        verbose_name_plural = 'Pokemons Matus Caught'

    def __str__(self):
        return "{} (#{})".format(self.name, self.pokemon_id)
