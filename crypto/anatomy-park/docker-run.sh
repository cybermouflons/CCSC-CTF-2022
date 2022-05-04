#!/bin/bash
IMAGE_NAME=cybermouflons/ccsc-2022-anatomy-park

docker run -p 9002:13373 -d --restart=always $IMAGE_NAME
