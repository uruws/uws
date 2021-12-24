#!/bin/sh
set -eu
BUILD_CACHE=${PWD}/docker/golang/build/cache
TMPDIR=${PWD}/tmp
mkdir -vp ${BUILD_CACHE} ${TMPDIR}
exec docker run -it --rm --name uws-golang-devel \
	--hostname go-devel.uws.local -u uws \
	-v ${TMPDIR}:/go/tmp \
	-v ${PWD}/go:/go/src/uws \
	-v ${BUILD_CACHE}:/go/.cache \
	-p 127.0.0.1:2800:2800 \
	-p 127.0.0.1:2801:2801 \
	--entrypoint /usr/local/bin/uws-login.sh \
	uws/golang-2109
