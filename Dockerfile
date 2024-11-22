FROM python:3.12-slim-bullseye AS builder

WORKDIR /app

COPY poetry.lock poetry.toml pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.8.4 \
    && poetry install --no-interaction --no-ansi

FROM python:3.12-slim-bullseye

COPY --from=builder /app /app
COPY cli/ src/ utils/

ENTRYPOINT [ "python", "-B", "-m", "cli" ]
CMD [ "--help" ]
