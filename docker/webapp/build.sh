#!/bin/sh
set -eu
# uws/webapp-2211
docker build --rm -t uws/webapp-2211 \
	-f docker/webapp/Dockerfile.2211 \
	./docker/webapp
exit 0
