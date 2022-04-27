FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y gcc-multilib socat

WORKDIR /root
COPY chall .
COPY flag.txt .

EXPOSE 1337
EXPOSE 1338
CMD ["socat", "-v", "-v","TCP-LISTEN:1337,reuseaddr,fork,su=root", "EXEC:'/root/chall'"]
