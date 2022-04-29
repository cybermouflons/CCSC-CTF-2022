FROM python:3

RUN mkdir /usr/app

WORKDIR /usr/app

COPY requirements.txt server.py Audio.py ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9001

CMD ["python","./server.py"]
