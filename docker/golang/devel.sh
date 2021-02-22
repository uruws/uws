#!/bin/sh
BUILD_CACHE=${PWD}/build/go-cache
mkdir -vp ${BUILD_CACHE}
exec docker run -it --rm --name uws-golang-devel \
	--hostname go-devel.uws.local -u uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	-v ${PWD}/go:/go/src/uws \
	-v ${BUILD_CACHE}:/go/.cache \
	uws/golang
