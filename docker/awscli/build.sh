#!/bin/sh
set -eu
# awscli
docker build "$@" --rm -t uws/awscli \
	--build-arg "UWS_UID=$(id -u)" \
	--build-arg "UWS_GID=$(id -g)" \
	--build-arg "UWS_UMASK=$(umask)" \
	-f docker/awscli/Dockerfile \
	./docker/awscli
# awscli-2203
docker build "$@" --rm -t uws/awscli-2203 \
	--build-arg "UWS_UID=$(id -u)" \
	--build-arg "UWS_GID=$(id -g)" \
	--build-arg "UWS_UMASK=$(umask)" \
	-f docker/awscli/Dockerfile.2203 \
	./docker/awscli
exit 0
