FROM python:3.11-slim-buster

WORKDIR /service
COPY poetry.toml pyproject.toml poetry.lock /service/
COPY ./app /service/app
RUN python3.11 -m pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry install --no-dev --no-interaction --no-ansi -vvv
CMD ["poetry", "run", "python", "-m", "app"]

EXPOSE 8080