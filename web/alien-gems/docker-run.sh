IMAGE_NAME=cybermouflons/ccsc2022-alien-gems

docker run -d --restart unless-stopped -p 3000:3000 ${IMAGE_NAME} 
