DISORD_BOT_IMAGE_NAME=cybermouflons/ccsc2022-pickle-rick-discord
PICKLE_RICK_IMAGE_NAME=cybermouflons/ccsc2022-pickle-rick-core

cat <<- EOF > docker-compose.override.yml
version: '3.5'
services:
  pickle-rick:
    image: ${PICKLE_RICK_IMAGE_NAME}
  
  discord-bot:
    image: ${DISORD_BOT_IMAGE_NAME}
EOF

docker-compose -f setup/docker-compose.yml -f docker-compose.override.yml build

rm docker-compose.override.yml