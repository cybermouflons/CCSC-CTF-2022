#!/bin/bash
# --security-opt=seccomp:unconfined
docker run -p 1234:1234 -d --restart=always ccsc2022/z3ep_xanflorp_i