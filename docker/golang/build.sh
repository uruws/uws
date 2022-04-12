#!/bin/sh
set -eu
mkdir -vp ./docker/golang/tmp
install -C -v -m 640 ./go/go.mod ./go/go.sum ./docker/golang/tmp/
docker rmi uws/golang-2109 || true
# golang-2203
docker build --rm -t uws/golang-2203 \
	-f ./docker/golang/Dockerfile.2203 ./docker/golang
exit 0
