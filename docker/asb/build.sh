#!/bin/sh
set -eu
docker rmi uws/ansible || true
# ansible-2203
docker build --rm -t uws/ansible-2203 \
	-f docker/asb/Dockerfile.2203 \
	./docker/asb
exit 0
