
FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat gcc-multilib

# set workdir and transfer binary
WORKDIR /root
COPY nohook .
COPY flag.txt .
COPY libc.so.6 .
COPY ld-linux-x86-64.so.2 .

EXPOSE 6337
CMD ["socat", "-v","TCP-LISTEN:6337,reuseaddr,fork,su=root", "EXEC:'/root/nohook'"]
