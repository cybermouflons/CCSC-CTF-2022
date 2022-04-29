FROM python:2.7

RUN apt-get update && apt-get install -y socat
RUN pip install pycrypto

# transfer files
WORKDIR /root
COPY encrypt.py ./encrypt.py

EXPOSE 3137
CMD ["socat", "-T60", "TCP-LISTEN:3137,reuseaddr,fork,su=root", "EXEC:'python -u encrypt.py'"]
