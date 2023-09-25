#!/bin/sh
set -eu
# remove old versions
docker rmi uws/cli-2211 || true
# uws/cli-2305
docker build --rm -t uws/cli-2305 \
	-f docker/uwscli/Dockerfile.2305 \
	./docker/uwscli
# uws/cli-2309
docker build --rm -t uws/cli-2309 \
	-f docker/uwscli/Dockerfile.2309 \
	./docker/uwscli
exit 0
