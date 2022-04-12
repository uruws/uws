#!/bin/sh
set -eu
docker rmi uws/mkcert || true
# mkcert-2203
docker build --rm -t uws/mkcert-2203 \
	-f docker/mkcert/Dockerfile.2203 \
	./docker/mkcert
exit 0
