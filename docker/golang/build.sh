#!/bin/sh
set -eu
mkdir -vp ./docker/golang/tmp
install -C -v -m 640 ./go/go.mod ./go/go.sum ./docker/golang/tmp/
# golang-2203
docker build --rm -t uws/golang-2203 \
	-f ./docker/golang/Dockerfile.2203 ./docker/golang
# golang-2211
docker build --rm -t uws/golang-2211 \
	-f ./docker/golang/Dockerfile.2211 ./docker/golang
exit 0
