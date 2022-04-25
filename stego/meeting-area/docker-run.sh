IMAGE_NAME=cybermouflons/meeting-area

docker run -d --restart unless-stopped -p 3000:3000 ${IMAGE_NAME} 
