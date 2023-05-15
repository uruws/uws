#!/bin/sh
set -eu
if test 'X0' = "X$(id -u)"; then
	echo "do not run as root!" >&2
	exit 1
fi
# base.2203
docker rm uws/base-2203 || true
# base.2211
docker build "$@" --rm -t uws/base-2211 \
	--build-arg "UWS_UID=$(id -u)" \
	--build-arg "UWS_GID=$(id -g)" \
	--build-arg "UWS_UMASK=$(umask)" \
	-f docker/base/Dockerfile.2211 \
	./docker/base
# base.2305
docker build "$@" --rm -t uws/base-2305 \
	--build-arg "UWS_UID=$(id -u)" \
	--build-arg "UWS_GID=$(id -g)" \
	--build-arg "UWS_UMASK=$(umask)" \
	-f docker/base/Dockerfile.2305 \
	./docker/base
exit 0
