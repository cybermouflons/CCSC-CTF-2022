FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y gcc-multilib socat

WORKDIR /root
COPY chall .
COPY flag.txt .

EXPOSE 5337
EXPOSE 5338
CMD ["socat", "-v", "-v","TCP-LISTEN:5337,reuseaddr,fork,su=root", "EXEC:'/root/chall'"]
