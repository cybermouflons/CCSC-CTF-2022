IMAGE_NAME=cybermouflons/ccsc2022-planet-tc39

docker build ./setup -t ${IMAGE_NAME}

CID=$(docker create ${IMAGE_NAME})

docker cp ${CID}:/ctf/challenge/static/planet-tc39.tar.gz ./public/
docker rm ${CID}