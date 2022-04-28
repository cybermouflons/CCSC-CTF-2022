FROM python:3.8.1-slim

RUN apt-get update

# transfer files
WORKDIR /root
COPY scrambleGenerator.py ./scrambleGenerator.py
COPY scrambleImage.py ./scrambleImage.py
COPY scrambleImage.pyc ./scrambleImage.pyc

EXPOSE 6910
CMD ["socat", "-T60", "TCP-LISTEN:6910,reuseaddr,fork,su=root", "EXEC:'python2.7 -u scrambleGenerator.py'"]