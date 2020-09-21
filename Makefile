COMPOSE = docker-compose

build:
	$(COMPOSE) build

run:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) down

enter:
	$(COMPOSE) exec web bash

createsuperuser:
	$(COMPOSE) exec web python manage.py createsuperuser

test:
	$(COMPOSE) exec -T web python manage.py test

linter-black:
	$(COMPOSE) exec -T web black .

linter-flake8:
	$(COMPOSE) exec -T web flake8 . --exclude venv

linter-isort:
	$(COMPOSE) exec -T web isort .

linter-mypy:
	$(COMPOSE) exec -T web mypy -p debunkbot --ignore-missing-imports

