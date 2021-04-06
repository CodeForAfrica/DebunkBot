COMPOSE = docker-compose

build:
	$(COMPOSE) build

run:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) down

enter:
	$(COMPOSE) exec app bash

createsuperuser:
	$(COMPOSE) exec app python manage.py createsuperuser

test:
	$(COMPOSE) exec -T app python manage.py test

linter-black:
	$(COMPOSE) exec -T app black .

linter-flake8:
	$(COMPOSE) exec -T app flake8 . --exclude venv

linter-isort:
	$(COMPOSE) exec -T app isort .

linter-mypy:
	$(COMPOSE) exec -T app mypy -p debunkbot --ignore-missing-imports
