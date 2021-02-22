#!/bin/sh
BUILD_CACHE=${PWD}/build/go-cache
mkdir -vp ${BUILD_CACHE}
exec docker run --rm --network none --name uws-golang-cmd \
	--hostname go-cmd.uws.local -u uws \
	-v ${PWD}/go:/go/src/uws \
	-v ${BUILD_CACHE}:/go/.cache \
	uws/golang $@
