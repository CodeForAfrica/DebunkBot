COMPOSE = docker-compose

build:
	$(COMPOSE) build

run:
	$(COMPOSE) up -d

enter:
	$(COMPOSE) exec app bash

createsuperuser:
	$(COMPOSE) exec app python manage.py createsuperuser

lint:
	$(COMPOSE) exec -T app pre-commit run --all-files

test:
	$(COMPOSE) exec -T app python manage.py test

stop:
	$(COMPOSE) down
