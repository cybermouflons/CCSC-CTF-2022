FROM python:3.8-slim

RUN pip install poetry

COPY pyproject.toml /chall/pyproject.toml
COPY poetry.lock /chall/poetry.lock

WORKDIR /chall

RUN poetry install

COPY . /chall

CMD ["poetry","run","python","bot.py"]