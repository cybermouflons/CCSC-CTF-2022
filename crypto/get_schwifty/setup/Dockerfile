FROM python:3.8.1-slim

RUN apt-get update

# transfer files
WORKDIR /root
COPY encrypt.py ./encrypt.py

EXPOSE 3137
CMD ["socat", "-T60", "TCP-LISTEN:3137,reuseaddr,fork,su=root", "EXEC:'python2.7 -u encrypt.py'"]