APP-NAME = performix
APP-VERSION = 1.0.0

PYTHON = python -B

# Компоненты
http:
	$(PYTHON) -m cli --start-http-api

crontab:
	$(PYTHON) -m cli --start-crontab

stream:
	$(PYTHON) -m cli --start-stream

grpc:
	$(PYTHON) -m cli --start-grpc-api

# Линтеры
lint: ruff mypy

mypy:
	$(PYTHON) -m mypy .

ruff:
	$(PYTHON) -m ruff check .

# Docker
docker-compose:
	docker build --tag $(APP-NAME):$(APP-VERSION) .
	docker compose down --remove-orphans
	docker compose up --build --force-recreate --remove-orphans
