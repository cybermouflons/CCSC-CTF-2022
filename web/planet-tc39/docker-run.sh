IMAGE_NAME=cybermouflons/ccsc2022-planet-tc39

docker run -d --restart unless-stopped -p 3000:3000 ${IMAGE_NAME} 
