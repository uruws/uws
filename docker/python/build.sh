#!/bin/sh
set -eu
docker rmi uws/python-2109 || true
# python-2203
docker build --rm -t uws/python-2203 \
	-f docker/python/Dockerfile.2203 \
	./docker/python
exit 0
