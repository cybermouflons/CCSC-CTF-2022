
FROM ubuntu

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat gcc-multilib

# set workdir and transfer binary
WORKDIR /root
COPY rickrop .
COPY flag.txt .

EXPOSE 3337
CMD ["socat", "-v","TCP-LISTEN:3337,reuseaddr,fork,su=root", "EXEC:'/root/rickrop'"]
