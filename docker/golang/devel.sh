#!/bin/sh
BUILD_CACHE=${PWD}/build/uws/cache
mkdir -vp ${BUILD_CACHE}
exec docker run -it --rm --name uws-golang-devel \
	--hostname golang-devel.uws.local -u uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	-v ${PWD}/src/uws:/go/src/uws \
	-v ${BUILD_CACHE}:/go/.cache \
	uws/golang
