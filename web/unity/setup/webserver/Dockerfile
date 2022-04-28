FROM python:3.7-alpine
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app/ /app
COPY flag.txt /
WORKDIR /app
CMD python3 app.py
