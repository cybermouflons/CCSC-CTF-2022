FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat gcc-multilib

# set workdir and transfer binary
WORKDIR /root
COPY pwn .
COPY heapAllocator.so .
COPY heapAllocator.so /usr/lib/
COPY flag.txt .

EXPOSE 1337

CMD ["socat", "-v","TCP-LISTEN:1337,reuseaddr,fork,su=root", "EXEC:'/root/pwn'"]