#!/bin/sh
set -eu
# cli
docker build --rm -t uws/cli \
	-f docker/uwscli/Dockerfile \
	./docker/uwscli
# cli-2203
docker build --rm -t uws/cli-2203 \
	-f docker/uwscli/Dockerfile.2203 \
	./docker/uwscli
exit 0
