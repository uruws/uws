#!/bin/sh
set -eu
# python-2109
docker build $@ --rm -t uws/python-2109 \
	-f docker/python/Dockerfile.2109 \
	./docker/python
exit 0
