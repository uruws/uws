#!/bin/sh
set -eu
# remove old versions
docker rmi uws/golang-2203 || true
# uws/golang-2211
docker build --rm -t uws/golang-2211 \
	-f docker/golang/Dockerfile.2211 \
	./docker/golang
# uws/golang-2305
docker build --rm -t uws/golang-2305 \
	-f docker/golang/Dockerfile.2305 \
	./docker/golang
exit 0
