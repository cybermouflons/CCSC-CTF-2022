FROM python:3.8-slim

WORKDIR /home/chall

COPY poetry.lock /home/chall
COPY pyproject.toml /home/chall

RUN pip install poetry 

RUN poetry install --no-dev

COPY . .

CMD ["poetry","run","python","challenge.py"]