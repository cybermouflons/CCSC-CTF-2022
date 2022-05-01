FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y socat gcc-multilib

RUN useradd -ms /bin/bash -u 58623 user

# transfer files
WORKDIR /home/user
COPY pwn ./pwn
COPY jail ./jail
COPY password.txt ./password.txt
COPY flag.txt ./flag.txt

RUN chown user:user ./pwn
RUN chmod u+s ./pwn

EXPOSE 13372
CMD ["socat", "-T60", "TCP-LISTEN:13372,reuseaddr,fork,su=user", "EXEC:/home/user/pwn"]
