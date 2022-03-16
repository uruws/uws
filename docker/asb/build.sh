#!/bin/sh
set -eu
# ansible
docker build --rm -t uws/ansible \
	-f docker/asb/Dockerfile \
	./docker/asb
# ansible-2203
docker build --rm -t uws/ansible-2203 \
	-f docker/asb/Dockerfile.2203 \
	./docker/asb
exit 0
