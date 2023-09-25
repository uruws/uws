#!/bin/sh
set -eu
_UID=$(id -u)
_GID=$(id -g)
_UMASK=$(umask)
_VERSION=$(cat ./docker/VERSION)
# awscli-2203
docker rmi uws/awscli-2203 || true
docker rmi uws/awscli-2211 || true
# awscli-2305
docker build "$@" --rm -t uws/awscli-2305 \
	--build-arg "UWS_UID=${_UID}" \
	--build-arg "UWS_GID=${_GID}" \
	--build-arg "UWS_UMASK=${_UMASK}" \
	--build-arg "UWS_VERSION=230710" \
	-f docker/awscli/Dockerfile.2305 \
	./docker/awscli
# awscli-2309
docker build "$@" --rm -t uws/awscli-2309 \
	--build-arg "UWS_UID=${_UID}" \
	--build-arg "UWS_GID=${_GID}" \
	--build-arg "UWS_UMASK=${_UMASK}" \
	--build-arg "UWS_VERSION=${_VERSION}" \
	-f docker/awscli/Dockerfile.2309 \
	./docker/awscli
exit 0
