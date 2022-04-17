FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y socat gcc-multilib python3 --fix-missing

# set workdir and transfer binary
WORKDIR /root
COPY chall.py .
COPY flag.txt .

EXPOSE 1338

CMD ["socat", "-v","TCP-LISTEN:1338,reuseaddr,fork,su=root", "EXEC:'python3 /root/chall.py'"]