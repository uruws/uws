#!/bin/sh
set -eu
# remove old versions
docker rmi uws/webapp-2211 || true
# uws/webapp-2305
docker build --rm -t uws/webapp-2305 \
	-f docker/webapp/Dockerfile.2305 \
	./docker/webapp
# uws/webapp-2309
docker build --rm -t uws/webapp-2309 \
	-f docker/webapp/Dockerfile.2309 \
	./docker/webapp
exit 0
