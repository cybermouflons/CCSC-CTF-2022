FROM ruby:3.1.1

WORKDIR /ctf/challenge

COPY ./demo /ctf/challenge

RUN bundle install

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y yarn

RUN yarn install --check-files

RUN adduser ctfuser
RUN chown ctfuser -R /ctf/challenge
USER ctfuser

ENV SECRET_TOKEN="no_chance_no_guess_0-0-0"
ENV SECRET_FLAG="CCSC{sapph1re_em3rald_ruby_diam0nd}"

CMD ["thin", "start"]