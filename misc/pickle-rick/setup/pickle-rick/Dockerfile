FROM cybermouflons/minideb-xinetd-python:0.1.0

COPY pickle_rick.py /root/chall/ 
COPY flag.txt /

WORKDIR /root/chall/ 

ENV ARGS "/root/chall/pickle_rick.py"
ENV PORT 4000