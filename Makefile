COMPOSE_FILE := "local.yml"


build:
	docker-compose -f $(COMPOSE_FILE) build

migrate:
	docker-compose -f $(COMPOSE_FILE) run --rm django python manage.py migrate

# ensures all services are running
runserver:
	docker-compose -f $(COMPOSE_FILE) up

make-migration:
	docker-compose -f $(COMPOSE_FILE) run --rm django python manage.py makemigrations

django-command:
	docker-compose -f local.yml run --rm django python manage.py $(command)

test:
	docker-compose -f $(COMPOSE_FILE) run django pytest --disable-warnings

teardown:
	docker-compose -f $(COMPOSE_FILE) down
