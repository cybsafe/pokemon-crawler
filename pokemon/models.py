from django.db import models


class PokemonMatusCaught(models.Model):  # personal touch :seenoevil:
    # Due to time constraints, lets capture only the following information
    pokemon_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=128)

