#!/bin/sh
set -eu
# mkcert
docker build --rm -t uws/mkcert \
	-f docker/mkcert/Dockerfile \
	./docker/mkcert
# mkcert-2203
docker build --rm -t uws/mkcert-2203 \
	-f docker/mkcert/Dockerfile.2203 \
	./docker/mkcert
exit 0
