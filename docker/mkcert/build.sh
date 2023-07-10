#!/bin/sh
set -eu
# remove old versions
docker rmi uws/mkcert-2211 || true
# uws/mkcert-2305
docker build --rm -t uws/mkcert-2305 \
	-f docker/mkcert/Dockerfile.2305 \
	./docker/mkcert
exit 0
