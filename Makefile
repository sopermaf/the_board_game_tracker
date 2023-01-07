COMPOSE_FILE := "local.yml"


build:
	docker-compose -f $(COMPOSE_FILE) build

migrate:
	$(MAKE) django-migrate

# ensures all services are running
runserver:
	docker-compose -f $(COMPOSE_FILE) up

makemigrations:
	$(MAKE) django-makemigrations

shell:
	$(MAKE) django-shell

django-%:
	docker-compose -f local.yml run --rm django python manage.py $*

test:
	docker-compose -f $(COMPOSE_FILE) run django pytest --disable-warnings

teardown:
	docker-compose -f $(COMPOSE_FILE) down
