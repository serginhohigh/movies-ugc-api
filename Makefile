COMPOSE = docker compose
COMPOSE_FILE = docker-compose.yml
COMPOSE_FILE_DEV = docker-compose.dev.yml
COMPOSE_FILE_TEST = tests/functional/docker-compose.yml

help: ## Show this help
	@printf "\033[33m%s:\033[0m\n" 'Available commands'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[32m%-11s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Remove python compiled cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

lint: ## Make lint with ruff and type check with mypy
	ruff .
	black . --check
	isort . --check
	mypy .

format: ## Trigger black formatter and isort util
	black .
	isort .

migrate: ## Initialize mongo sharded cluster
	docker exec -i mongocfg1 mongosh < mongo/init_config.js
	docker exec -i mongors1n1 mongosh < mongo/init_shard1.js
	docker exec -i mongors2n1 mongosh < mongo/init_shard2.js
	docker exec -i mongos1 mongosh < mongo/add_shards.js
	docker exec -i mongos1 mongosh < mongo/init_database.js
	docker exec -i mongos1 mongosh < mongo/enable_sharding.js

install: ## Prepare prod env
	cp .env.example .env
	cp ./ugc/.env.example ./ugc/.env
	cp ./tests/functional/.env.example ./tests/functional/.env

test: ## Run functional tests
	${COMPOSE} -f ${COMPOSE_FILE_TEST} run --quiet-pull --rm --build \
		pytest bash -c 'python3 utils/wait_for_mongo.py; pytest -vv -s'; \
		${COMPOSE} -f ${COMPOSE_FILE_TEST} down

up: ## UP prod containers
	${COMPOSE} up -d --build

down: ## Down prod containers
	${COMPOSE} down

restart: ## Restart prod containers
	${COMPOSE} down
	${COMPOSE} up -d

dev-up: ## UP dev containers
	${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} up -d $(c) --build

dev-stop: ## Stop dev container
	${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} stop $(c) \
		&& ${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} rm -f $(c)

dev-down: ## Down dev containers
	${COMPOSE} -f ${COMPOSE_FILE} -f ${COMPOSE_FILE_DEV} down
