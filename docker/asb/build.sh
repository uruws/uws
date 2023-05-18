#!/bin/sh
set -eu
# remove old versions
docker rmi uws/ansible-2203 || true
# uws/ansible-2211
docker build --rm -t uws/ansible-2211 \
	-f docker/asb/Dockerfile.2211 \
	./docker/asb
# uws/ansible-2305
docker build --rm -t uws/ansible-2305 \
	-f docker/asb/Dockerfile.2305 \
	./docker/asb
exit 0
