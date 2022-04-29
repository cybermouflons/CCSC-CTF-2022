#!/bin/bash
# --security-opt=seccomp:unconfined
docker run -p 3137:3137 -d --restart=always ccsc2022/get_schwifty
