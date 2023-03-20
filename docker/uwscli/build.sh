#!/bin/sh
set -eu
# remove old versions
docker rmi uws/cli-2109 || true
# uws/cli-2203
docker build --rm -t uws/cli-2203 \
	-f docker/uwscli/Dockerfile.2203 \
	./docker/uwscli
# uws/cli-2211
docker build --rm -t uws/cli-2211 \
	-f docker/uwscli/Dockerfile.2211 \
	./docker/uwscli
exit 0
