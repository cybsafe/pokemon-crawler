from django.db import models


class PokemonType(models.Model):
    name = models.CharField(max_length=125)
    url = models.URLField(null=True)
    slot = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class PokemonAbility(models.Model):
    name = models.CharField(max_length=125)
    url = models.URLField(null=True)
    is_hidden = models.BooleanField(null=True)

    def __str__(self):
        return self.name


class Pokemon(models.Model):
    pokemon_id = models.IntegerField()
    name = models.CharField(max_length=250)
    is_default = models.BooleanField()
    base_experience = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)

    types = models.ManyToManyField(
        PokemonType,
        related_name='pokemon_types',
    )
    abilities = models.ManyToManyField(
        PokemonAbility,
        related_name='pokemon_abilities',
    )

    def __str__(self):
        return self.name
