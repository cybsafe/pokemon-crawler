import aiohttp
import asyncio
import requests


async def get_pokemon(session, pokemon_url):
    async with session.get(pokemon_url) as req:
        data = await req.json()
        return {
            "id": data.get('id'),
            "name": data.get("name"),
            "height": data.get("height"),
            "weight": data.get("weight"),
            "description": await get_pokemon_description(session, data.get("stats"))
        }

# There are only so many stats out there. Cache/memoise these
# for speed improvements
async def get_pokemon_description(session, stats, language="en"):
    max_stat = max(stats, key=lambda x: x["base_stat"] + x["effort"])
    async with session.get(max_stat["stat"]["url"]) as stat_req:
        stat_data = await stat_req.json()

        characteristic_urls_tasks = (
            get_characteristic_description(session, i["url"], language)
            for i in stat_data.get("characteristics", [])
        )
    description = "; ".join(await asyncio.gather(*characteristic_urls_tasks))
    return description

# There are only so many characteristics out there. Cache/memoise these
# for speed improvements
async def get_characteristic_description(session, characteristic_url, language="en"):
    async with session.get(characteristic_url) as characteristic_req:
        characteristic = await characteristic_req.json()
        for description in characteristic.get("descriptions", []):
            if description['language']["name"] == language:
                return description["description"]

    return ""


async def list_pokemon():
    # This is all sequential at the moment and very slow.
    # await/async is probably the way forward.
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://pokeapi.co/api/v2/pokemon/") as req:
            data = await req.json()
            tasks = []
            for pokemon in data["results"]:
                tasks.append(asyncio.ensure_future(get_pokemon(session, pokemon['url'])))
            results = await asyncio.gather(*tasks)
            yield results

    # yield [get_pokemon(pokemon['url']) for pokemon in data['results']]

        while data['next']:
            async with session.get(data["next"]) as req:
                data = await req.json()
                tasks = []
                for pokemon in data["results"]:
                    tasks.append(asyncio.ensure_future(get_pokemon(session, pokemon['url'])))
                results = await asyncio.gather(*tasks)
                yield results
