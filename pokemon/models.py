from django.db import models


class Pokemon(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    height = models.IntegerField()
    weight = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name
