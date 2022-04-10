FROM node:alpine3.14

COPY ./index.html /ctf/challenge/index.html
WORKDIR /ctf/challenge

RUN addgroup -S ctfgroup && adduser -S ctfuser -G ctfgroup
RUN chown ctfuser -R /ctf/
USER ctfuser


CMD [ "npx", "http-server", "-p", "3000"]