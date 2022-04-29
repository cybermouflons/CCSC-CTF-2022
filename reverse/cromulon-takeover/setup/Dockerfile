FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y gcc-multilib

WORKDIR /root
COPY chall .

EXPOSE 1337
# CMD ["socat", "-vv","TCP-LISTEN:1337,reuseaddr,fork,su=root", "EXEC:'/root/pwn'"]
CMD ["/root/chall", "71337"]
