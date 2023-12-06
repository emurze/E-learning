# Variables

DEFAULT_COLOR=\e[0m

BLUE=\e[34m

YELLOW=\033[33m

DOCKER_CONTAINER_NAME=e-learning

DOCKER_NAME_LINE=$$(echo "e-learning" | tr '[:graph:]' '-')


# Functions

define raise_container_does_not_exist
	echo "\n----------------------------------------------------${DOCKER_NAME_LINE}\n" && \
	echo "${YELLOW}Error docker container ${DOCKER_CONTAINER_NAME} does not exist. Use ${BLUE}make run${DEFAULT_COLOR}" && \
	echo "\n----------------------------------------------------${DOCKER_NAME_LINE}\n" && \
	exit 1
endef


# Run

run:
	docker compose up -d --build

run-prod:
	docker compose -f docker-compose.prod.yml up -d --build


# Migrations

migrations:
	@if [ -z $$(docker ps -q -f name=${DOCKER_CONTAINER_NAME}) ]; then \
		$(call raise_container_does_not_exist); \
	else \
		docker exec ${DOCKER_CONTAINER_NAME} bash -c "cd src && poetry run python3 manage.py makemigrations"; \
	fi

migrate:
	@if [ -z $$(docker ps -q -f name=${DOCKER_CONTAINER_NAME}) ]; then \
		$(call raise_container_does_not_exist); \
	else \
		docker exec ${DOCKER_CONTAINER_NAME} bash -c "cd src && poetry run python3 manage.py migrate"; \
	fi


# Restart | Down

restart:
	docker compose restart

restart-prod:
	docker compose -f docker-compose.prod.yml restart

down:
	docker compose down

down-prod:
	docker compose -f docker-compose.prod.yml down

clean:
	docker compose down -v
	docker compose -f docker-compose.prod.yml down -v


# Tests | You can run tests only if you have previously run container

lint:
	@if [ -z $$(docker ps -q -f name=${DOCKER_CONTAINER_NAME}) ]; then \
		$(call raise_container_does_not_exist); \
	else \
		poetry run flake8 --config setup.cfg src tests; \
	fi

unittests:
	@if [ -z $$(docker ps -q -f name=${DOCKER_CONTAINER_NAME}) ]; then \
		$(call raise_container_does_not_exist); \
	else \
		docker exec ${DOCKER_CONTAINER_NAME} bash -c "cd src && poetry run python3 manage.py test ${path}"; \
	fi

coverage:
	@if [ -z $$(docker ps -q -f name=${DOCKER_CONTAINER_NAME}) ]; then \
		$(call raise_container_does_not_exist); \
	else \
		docker exec ${DOCKER_CONTAINER_NAME} bash -c "cd src && poetry run coverage run --rcfile ../setup.cfg --data-file logs/.coverage manage.py test ${path} && poetry run coverage report --rcfile ../setup.cfg --data-file logs/.coverage"; \
	fi

e2etests:
	@if [ -z $$(docker ps -q -f name=${DOCKER_CONTAINER_NAME}) ]; then \
		$(call raise_container_does_not_exist); \
	else \
		docker exec ${DOCKER_CONTAINER_NAME} bash -c "poetry run python3 src/manage.py test tests/${path}"; \
	fi

test: lint coverage e2etests
