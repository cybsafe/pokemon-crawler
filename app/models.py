from django.db import models


class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    attack = models.IntegerField()
    special_attack = models.IntegerField()
    defense = models.IntegerField()
    weight = models.IntegerField()
    move = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
