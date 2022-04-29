#!/bin/bash
# --security-opt=seccomp:unconfined
docker run -p 6910:6910 -d --restart=always ccsc2022/cubik_rick
