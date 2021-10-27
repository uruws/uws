#!/bin/sh
BUILD_CMD=${PWD}/docker/golang/build
BUILD_CACHE=${PWD}/docker/golang/build/cache
mkdir -vp ${BUILD_CACHE} ${BUILD_CMD}
exec docker run --rm --network none --name uws-golang-cmd \
	--hostname go-cmd.uws.local -u uws \
	-v ${PWD}/go:/go/src/uws \
	-v ${BUILD_CACHE}:/go/.cache \
	-v ${BUILD_CMD}:/go/build/cmd \
	uws/golang-2109 $@
