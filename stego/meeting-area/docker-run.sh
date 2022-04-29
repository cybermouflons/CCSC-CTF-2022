IMAGE_NAME=cybermouflons/meeting-area

docker run -d --restart unless-stopped -p 3002:3000 ${IMAGE_NAME} 
