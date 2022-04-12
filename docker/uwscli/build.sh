#!/bin/sh
set -eu
docker rmi uws/cli || true
# cli-2203
docker build --rm -t uws/cli-2203 \
	-f docker/uwscli/Dockerfile.2203 \
	./docker/uwscli
exit 0
