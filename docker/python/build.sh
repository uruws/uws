#!/bin/sh
set -eu
# remove old versions
docker rmi uws/python-2211 || true
# uws/python-2305
docker build --rm -t uws/python-2305 \
	-f docker/python/Dockerfile.2305 \
	./docker/python
# uws/python-2309
docker build --rm -t uws/python-2309 \
	-f docker/python/Dockerfile.2309 \
	./docker/python
exit 0
