PYTHON = python -B

# Компоненты
api:
	$(PYTHON) -m cli --start-api

crontab:
	$(PYTHON) -m cli --start-crontab

stream:
	$(PYTHON) -m cli --start-stream

grpc:
	$(PYTHON) -m cli --start-grpc

# Линтеры
lint: ruff mypy

mypy:
	mypy .

ruff:
	ruff check .
