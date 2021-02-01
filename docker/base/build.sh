#!/bin/sh
set -eu
exec docker build --pull --rm -t uws/base \
	--build-arg UWS_UID=$(id -u) \
	--build-arg UWS_GID=$(id -g) \
	--build-arg UWS_UMASK=$(umask) \
	./docker/base
