FROM python:3.8-slim

WORKDIR /chall

RUN pip install poetry

COPY . .

RUN poetry install

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]


