ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif
HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

# Commands
env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.example .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

dev: ##@Environment Install all deps
	poetry install
	poetry run pre-commit install

up-dev:  ##@Database Create databases with docker-compose
	docker-compose -f dev.docker-compose.yml up -d --remove-orphans
	
down-dev: ##@Database Shutdown databases with docker-compose
	docker-compose -f dev.docker-compose.yml down --remove-orphans

up-prod:  ##@Database Create databases and build app with docker-compose
	docker-compose -f prod.docker-compose.yml up -d --remove-orphans --force-recreate --build app

down-prod: ##@Database Shutdown databases and app with docker-compose
	docker-compose -f prod.docker-compose.yml down --remove-orphans

lint:  ##@Code Check code with mypy
	poetry run python3 -m mypy --ignore-missing-imports app tests

test: ##@Code Test code
	make up
	poetry run python3 -m pytest --verbosity=2 --showlocals -log-level=DEBUG --cov=app --cov-report term  --cov-fail-under=70

format:  ##@Code Reformat code with black
	poetry run python3 -m black app tests

migrate:  ##@Database Do all migrations in database
	alembic -c app/db/alembic.ini upgrade $(args)

run:  ##@Application Run application server
	poetry run uvicorn app.__main__:app --host localhost --port 80 --reload --reload-dir app --reload-dir tests
open_db:  ##@Database Open database inside docker-image
	docker exec -it postgres-container psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

revision:  ##@Database Create new revision file automatically with prefix (ex. 2022_01_01_14cs34f_message.py)
	alembic -c app/db/alembic.ini revision --autogenerate

%::
	echo $(MESSAGE)
