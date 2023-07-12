#!/bin/sh
set -eu
BUILD_CMD=${PWD}/docker/golang/build
BUILD_CACHE=${PWD}/docker/golang/build/cache
BUILD_TMP=${PWD}/docker/golang/tmp
mkdir -vp ${BUILD_CACHE} ${BUILD_CMD} ${BUILD_TMP}
exec docker run --rm --network none --name uws-golang-cmd \
	--hostname go-cmd.uws.local -u uws \
	--read-only \
	-v ${PWD}/go:/go/src/uws:ro \
	-v ${BUILD_CACHE}:/go/.cache \
	-v ${BUILD_TMP}:/tmp \
	-v ${BUILD_CMD}:/go/build/cmd \
	-e CGO_ENABLED=0 \
	uws/golang-2305 "$@"
