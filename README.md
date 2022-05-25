# Pokemon Crawler

Project started from https://docs.docker.com/compose/django/

Some useful commands:

* `docker-compose up`
* `docker-compose exec web bash`
* `docker-compose exec web python -m pip install -r requirements.txt`


## How it works

- Initial population is done via a data migration which calls the Pokemon API
- A management command for the pokemon app is available to update Pokemon info
    `docker compose exec web python manage.py update_pokemon`
- List and detail views of the pokemon data held is available at `/pokemon/` and `/pokemon/<id>`
- Pokemon API access is asynchronous (asyncio and aiohttp) to improve data ingestion speeds.



## Improvements
- Add some checking to migration + roll back
- Schedule update job to run regularly in the background (Celery or similar depending on environment)
- Make pokemon page sizes configurable
- Logging
- Pre-commit hooks to run tests and do some linting
