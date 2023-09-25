#!/bin/sh
set -eu
# remove old versions
docker rmi uws/golang-2211 || true
# uws/golang-2305
docker build --rm -t uws/golang-2305 \
	-f docker/golang/Dockerfile.2305 \
	./docker/golang
# uws/golang-2309
docker build --rm -t uws/golang-2309 \
	-f docker/golang/Dockerfile.2309 \
	./docker/golang
exit 0
