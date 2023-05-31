#!/bin/sh
set -eu
_VERSION=$(cat ./docker/VERSION)
exec docker build --rm -t uws/pod:base \
	--build-arg "UWS_VERSION=${_VERSION}" \
	./pod/base
