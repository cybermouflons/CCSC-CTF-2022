FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y socat gcc-multilib

# transfer files
WORKDIR /root
COPY pwn ./pwn
COPY flag.txt ./flag.txt

EXPOSE 4337
CMD ["socat", "-T60", "TCP-LISTEN:4337,reuseaddr,fork,su=root", "EXEC:/root/pwn"]
