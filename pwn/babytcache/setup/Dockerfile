
FROM ubuntu

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat gcc-multilib

# set workdir and transfer binary
WORKDIR /root
COPY babytcache .
COPY ld-linux-x86-64.so.2 .
COPY flag.txt .
COPY libc.so.6 .

EXPOSE 2337
CMD ["socat", "-v","TCP-LISTEN:2337,reuseaddr,fork,su=root", "EXEC:'/root/babytcache'"]
