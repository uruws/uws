#!/bin/sh
set -eu
# remove old versions
docker rmi uws/webapp-2203 || true
# uws/webapp-2211
docker build --rm -t uws/webapp-2211 \
	-f docker/webapp/Dockerfile.2211 \
	./docker/webapp
# uws/webapp-2305
docker build --rm -t uws/webapp-2305 \
	-f docker/webapp/Dockerfile.2305 \
	./docker/webapp
exit 0
