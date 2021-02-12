#!/bin/sh
BUILD_CACHE=${PWD}/build/uws/cache
mkdir -vp ${BUILD_CACHE}
exec docker run --rm --network none --name uws-golang-cmd \
	--hostname golang-cmd.uws.local -u uws \
	-v ${PWD}/src/uws:/go/src/uws \
	-v ${BUILD_CACHE}:/go/.cache \
	uws/golang $@
