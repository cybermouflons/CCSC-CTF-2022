FROM python:2.7

RUN apt-get update && apt-get install -y socat

# transfer files
WORKDIR /root
COPY scrambleGenerator.py ./scrambleGenerator.py
COPY scrambleImage.py ./scrambleImage.py
COPY scrambleImage.pyc ./scrambleImage.pyc

EXPOSE 6910
CMD ["socat", "-T60", "TCP-LISTEN:6910,reuseaddr,fork,su=root", "EXEC:'python2.7 -u scrambleGenerator.py'"]
