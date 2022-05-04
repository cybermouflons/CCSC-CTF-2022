FROM python:3.8-alpine

RUN apk update
RUN apk add socat

# transfer files
WORKDIR /root
COPY app.py ./app.py
COPY flag.txt ./flag.txt

EXPOSE 13373
CMD ["socat", "-T60", "TCP-LISTEN:13373,reuseaddr,fork,su=root", "EXEC:python3 app.py"]
