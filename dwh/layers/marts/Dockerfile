FROM python:3.12-slim-bullseye

WORKDIR /app

RUN apt-get --yes update \
    && apt-get --yes install curl

COPY pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.8.4 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./ ./

ENTRYPOINT [ "python", "-B", "-m", "cli" ]
CMD [ "--help" ]
