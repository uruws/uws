#!/bin/sh
set -eu
_UID=$(id -u)
_GID=$(id -g)
_UMASK=$(umask)
_VERSION=$(cat ./docker/VERSION)
exec docker build --rm -t uws/base-testing \
	--build-arg "UWS_UID=${_UID}" \
	--build-arg "UWS_GID=${_GID}" \
	--build-arg "UWS_UMASK=${_UMASK}" \
	--build-arg "UWS_VERSION=${_VERSION}" \
	./docker/base-testing
