import requests


def get_pokemon(pokemon_url):
    data = requests.get(pokemon_url).json()
    return {
        "id": data.get('id'),
        "name": data.get("name"),
        "height": data.get("height"),
        "weight": data.get("weight"),
        "description": get_pokemon_description(data.get("stats"))
    }

# There are only so many characteristics out there. Cache/memoise these
# for speed improvements
def get_pokemon_description(stats, language="en"):
    max_stat = max(stats, key=lambda x: x["base_stat"] + x["effort"])
    stat_data = requests.get(max_stat["stat"]["url"]).json()
    characteristic_urls = [i["url"] for i in stat_data.get("characteristics", [])]
    description = "; ".join(
        [
            get_characteristic_description(url, language)
            for url in characteristic_urls
        ]
    )
    return description

# There are only so many characteristics out there. Cache/memoise these
# for speed improvements
def get_characteristic_description(characteristic_url, language="en"):
    characteristic = requests.get(characteristic_url)
    for description in characteristic.json().get("descriptions", []):
        if description['language']["name"] == language:
            return description["description"]

    return description


def list_pokemon():
    # This is all sequential at the moment and very slow.
    # await/async is probably the way forward.
    data = requests.get(f"https://pokeapi.co/api/v2/pokemon/?limit=1").json()
    yield [get_pokemon(pokemon['url']) for pokemon in data['results']]

    # while data['next']:
    if data['next']:
        data = requests.get(data["next"]).json()
        yield [get_pokemon(pokemon['url']) for pokemon in data['results']]
