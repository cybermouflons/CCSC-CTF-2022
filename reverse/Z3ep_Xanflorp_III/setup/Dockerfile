FROM ubuntu:20.04
RUN dpkg --add-architecture i386
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y gcc-multilib
RUN apt-get install -y libssl-dev
RUN apt-get install -y libssl-dev:i386
RUN apt-get install -y make

WORKDIR /usr/app

COPY makefile .
COPY vault.c .
RUN make
RUN chmod +x vault

EXPOSE 10002

CMD ["./vault"]
