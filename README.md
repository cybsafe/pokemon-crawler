# Pokemon Crawler

Project started from https://docs.docker.com/compose/django/

Some useful commands:

* `docker-compose up`
* `docker-compose exec web bash`
* `docker-compose exec web python -m pip install -r requirements.txt`

## Quickstart

## Development

1. (recommended) Set up a virtual environment:
   ```shell
   python -m venv venv
   source venv/bin/activate
   ```
2. Install and activate pre-commits:
   ```shell
   pip install -r requirements-dev.txt
   pre-commit install
   pre-commit install --hook-type commit-msg  # require explicit install, as per https://github.com/compilerla/conventional-pre-commit
   ```


Run tests:

```shell
docker-compose exec web python manage.py test
```
