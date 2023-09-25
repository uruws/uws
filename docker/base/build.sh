#!/bin/sh
set -eu
if test 'X0' = "X$(id -u)"; then
	echo "do not run as root!" >&2
	exit 1
fi
_UID=$(id -u)
_GID=$(id -g)
_UMASK=$(umask)
# base.2203
docker rmi uws/base-2203 || true
# base.2211
docker build "$@" --rm -t uws/base-2211 \
	--build-arg "UWS_UID=${_UID}" \
	--build-arg "UWS_GID=${_GID}" \
	--build-arg "UWS_UMASK=${_UMASK}" \
	-f docker/base/Dockerfile.2211 \
	./docker/base
# base.2305
_VERSION=$(cat ./docker/VERSION.2305)
docker build "$@" --rm -t uws/base-2305 \
	--build-arg "UWS_UID=${_UID}" \
	--build-arg "UWS_GID=${_GID}" \
	--build-arg "UWS_UMASK=${_UMASK}" \
	--build-arg "UWS_VERSION=${_VERSION}" \
	-f docker/base/Dockerfile.2305 \
	./docker/base
# base.2309
_VERSION=$(cat ./docker/VERSION)
docker build "$@" --rm -t uws/base-2309 \
	--build-arg "UWS_UID=${_UID}" \
	--build-arg "UWS_GID=${_GID}" \
	--build-arg "UWS_UMASK=${_UMASK}" \
	--build-arg "UWS_VERSION=${_VERSION}" \
	-f docker/base/Dockerfile.2309 \
	./docker/base
exit 0
