APP-NAME = sorting-hat
APP-VERSION = 1.0.0

PYTHON = python -B

# Компоненты
http-api:
	$(PYTHON) -m cli --start-http-api

crontab:
	$(PYTHON) -m cli --start-crontab

stream:
	$(PYTHON) -m cli --start-stream

grpc-api:
	$(PYTHON) -m cli --start-grpc-api

# Контейнеризация
docker:
	docker build --tag $(APP-NAME):$(APP-VERSION) .
	docker compose down --remove-orphans
	docker compose up --build --force-recreate --remove-orphans

# Линтеры
lint: ruff mypy

mypy:
	$(PYTHON) -m mypy .

ruff:
	$(PYTHON) -m ruff check .
