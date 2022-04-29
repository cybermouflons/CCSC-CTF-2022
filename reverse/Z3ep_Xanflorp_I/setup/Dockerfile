FROM python:3.8.1-slim

RUN apt-get update
RUN apt-get -y install socat
RUN python -m pip install angr
RUN python -m pip install numpy

# transfer files
WORKDIR /root
COPY z3_a.py .

EXPOSE 1234
CMD ["socat", "-T60", "TCP-LISTEN:1234,reuseaddr,fork,su=root", "EXEC:'python z3_a.py'"]