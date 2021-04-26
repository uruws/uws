#!/bin/sh
set -eu
if test 'X0' = "X$(id -u)"; then
	echo "do not run as root!" >&2
	exit 1
fi
exec docker build $@ --rm -t uws/base \
	--build-arg UWS_UID=$(id -u) \
	--build-arg UWS_GID=$(id -g) \
	--build-arg UWS_UMASK=$(umask) \
	./docker/base
