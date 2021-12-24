#!/bin/sh
set -eu
BUILD_CACHE=${PWD}/docker/golang/build/cache
BUILD_TMP=${PWD}/docker/golang/tmp
TMPDIR=${PWD}/tmp
mkdir -vp ${BUILD_CACHE} ${TMPDIR} ${BUILD_TMP}
exec docker run -it --rm --name uws-golang-devel \
	--hostname go-devel.uws.local -u uws \
	--read-only \
	-v ${PWD}/go:/go/src/uws:ro \
	-v ${BUILD_CACHE}:/go/.cache \
	-v ${BUILD_TMP}:/tmp \
	-v ${TMPDIR}:/go/tmp \
	-e CGO_ENABLED=0 \
	--entrypoint /usr/local/bin/uws-login.sh \
	-p 127.0.0.1:2800:2800 \
	-p 127.0.0.1:2801:2801 \
	uws/golang-2109
