#!/bin/bash
set -e

if [ -f demo/tmp/pids/server.pid ]; then
  rm demo/tmp/pids/server.pid
fi

thin start