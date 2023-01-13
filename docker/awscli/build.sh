#!/bin/sh
set -eu
# awscli-2203
docker build "$@" --rm -t uws/awscli-2203 \
	--build-arg "UWS_UID=$(id -u)" \
	--build-arg "UWS_GID=$(id -g)" \
	--build-arg "UWS_UMASK=$(umask)" \
	-f docker/awscli/Dockerfile.2203 \
	./docker/awscli
# awscli-2211
docker build "$@" --rm -t uws/awscli-2211 \
	--build-arg "UWS_UID=$(id -u)" \
	--build-arg "UWS_GID=$(id -g)" \
	--build-arg "UWS_UMASK=$(umask)" \
	-f docker/awscli/Dockerfile.2211 \
	./docker/awscli
exit 0
