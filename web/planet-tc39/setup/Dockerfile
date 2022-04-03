FROM node:alpine3.14

COPY . /ctf/challenge
WORKDIR /ctf/challenge

RUN addgroup -S ctfgroup && adduser -S ctfuser -G ctfgroup
RUN chown ctfuser -R /ctf/
USER ctfuser

RUN mv .env .tmp-env
RUN sed 's/{.*}/{FAKE_FLAG}/i' .tmp-env > .env
RUN tar -cf ./static/planet-tc39.tar.gz --exclude='.tmp-env' .
RUN mv .tmp-env .env

RUN npm install --ignore-scripts

CMD [ "npm", "run", "start", "app.js" ]