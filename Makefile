COMPOSE_FILE ?= "local.yml"


build:
	docker-compose -f $(COMPOSE_FILE) build

migrate:
	$(MAKE) django-migrate $(args)

# ensures all services are running
runserver:
	docker-compose -f $(COMPOSE_FILE) up

stop:
	docker-compose -f $(COMPOSE_FILE) stop

production-update: build stop migrate
	docker-compose -f $(COMPOSE_FILE) up -d

logs-follow:
	docker-compose -f $(COMPOSE_FILE) logs -f $(container)

makemigrations:
	$(MAKE) django-makemigrations

shell:
	$(MAKE) django-shell

django-%:
	docker-compose -f $(COMPOSE_FILE) run --rm django python manage.py $* $(args)

test:
	docker-compose -f $(COMPOSE_FILE) run django pytest --disable-warnings

teardown:
	docker-compose -f $(COMPOSE_FILE) down
