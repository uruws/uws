#!/bin/sh
set -eu
# cli
#docker build --rm -t uws/cli \
#	-f docker/uwscli/Dockerfile \
#	./docker/uwscli
docker rmi uws/cli || true
# cli-2203
docker build --rm -t uws/cli-2203 \
	-f docker/uwscli/Dockerfile.2203 \
	./docker/uwscli
exit 0
