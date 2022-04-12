#!/bin/sh
set -eu
if test 'X0' = "X$(id -u)"; then
	echo "do not run as root!" >&2
	exit 1
fi
docker rmi uws/base-2109 || true
# base.2203
docker build "$@" --rm -t uws/base-2203 \
	--build-arg "UWS_UID=$(id -u)" \
	--build-arg "UWS_GID=$(id -g)" \
	--build-arg "UWS_UMASK=$(umask)" \
	-f docker/base/Dockerfile.2203 \
	./docker/base
exit 0
