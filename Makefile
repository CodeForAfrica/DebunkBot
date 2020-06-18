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
