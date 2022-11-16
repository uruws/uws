#!/bin/sh
set -eu
# remove old versions
docker rmi uws/mkcert-2109 || true
# uws/mkcert-2203
docker build --rm -t uws/mkcert-2203 \
	-f docker/mkcert/Dockerfile.2203 \
	./docker/mkcert
# uws/mkcert-2211
docker build --rm -t uws/mkcert-2211 \
	-f docker/mkcert/Dockerfile.2211 \
	./docker/mkcert
exit 0
