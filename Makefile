COMPOSE_FILE ?= "local.yml"

pip-compile=.venv/bin/pip-compile

.venv:
	python -m venv .venv
	pip install -r requirements/base.txt
	pip install -r requirements/local.txt

build:
	docker compose -f $(COMPOSE_FILE) build

migrate:
	$(MAKE) django-migrate $(args)

# ensures all services are running
runserver:
	docker compose -f $(COMPOSE_FILE) up

stop:
	docker compose -f $(COMPOSE_FILE) stop

production-update: build stop migrate
	docker compose -f $(COMPOSE_FILE) up -d

logs-follow:
	docker compose -f $(COMPOSE_FILE) logs -f $(container)

makemigrations:
	$(MAKE) django-makemigrations

shell:
	$(MAKE) django-shell_plus

django-%:
	docker compose -f $(COMPOSE_FILE) run --rm django python manage.py $* $(args)

test:
	docker compose -f $(COMPOSE_FILE) run django pytest $(args)

teardown:
	docker compose -f $(COMPOSE_FILE) down

pip-compile:
	$(pip-compile) requirements/base.in
	$(pip-compile) requirements/production.in
	$(pip-compile) requirements/local.in

pip-compile-upgrade:
	$(pip-compile) --upgrade requirements/base.in
	$(pip-compile) --upgrade requirements/production.in
	$(pip-compile) --upgrade requirements/local.in

pip-sync:
	$(pip-sync) requirements/base.txt requirements/local.txt

mypy:
	docker compose -f local.yml run django mypy .


requirements-bump:
	$(MAKE) pip-compile-upgrade
	pre-commit run --all-files
	$(MAKE) build
	$(MAKE) test
	$(MAKE) mypy
