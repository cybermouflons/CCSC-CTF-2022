#!/bin/bash
# --security-opt=seccomp:unconfined
docker run -p 3137:3137 -d --restart=always ccsc2021/get_schwifty