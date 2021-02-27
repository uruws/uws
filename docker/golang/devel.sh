#!/bin/sh
set -eu
BUILD_CACHE=${PWD}/build/go-cache
mkdir -vp ${BUILD_CACHE}
exec docker run -it --rm --name uws-golang-devel \
	--hostname go-devel.uws.local -u uws \
	-v ${PWD}/go:/go/src/uws \
	-v ${BUILD_CACHE}:/go/.cache \
	-p 127.0.0.1:6060:6060 \
	--entrypoint /usr/local/bin/uws-login.sh \
	uws/golang
