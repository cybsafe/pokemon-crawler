from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from pokemon.models import Pokemon, PokemonAbility, PokemonType
from pokemon.serializers import PokemonSerializer


class TransactionsTemplateHTMLRender(TemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        response = renderer_context['response']
        if response.exception:
            data['status_code'] = response.status_code
        return {'pokemons': data}


class ListPokemonView(generics.ListCreateAPIView):
    queryset = Pokemon.objects.all().prefetch_related('abilities', 'types')
    serializer_class = PokemonSerializer
    template_name = 'list_pokemon.html'
    context_object_name = 'pokemon_list'
    renderer_classes = [TransactionsTemplateHTMLRender]


class RemovePokemonView(generics.DestroyAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    def perform_destroy(self, instance):
        Pokemon.objects.destroy()
        PokemonType.objects.destroy()
        PokemonAbility.objects.destroy()
