FROM node:alpine3.14

COPY . /ctf/challenge
WORKDIR /ctf/challenge

RUN addgroup -S ctfgroup && adduser -S ctfuser -G ctfgroup
RUN chown ctfuser -R /ctf/
USER ctfuser

RUN tar -cf ./planet-tc39.tar.gz --exclude='.env' .

RUN npm install --ignore-scripts

CMD [ "npm", "run", "start", "app.js" ]