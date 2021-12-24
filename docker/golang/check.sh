#!/bin/sh
set -eu
BUILD_CACHE=${PWD}/docker/golang/build/cache
TMPDIR=${PWD}/tmp
mkdir -vp ${BUILD_CACHE} ${TMPDIR}
exec docker run --rm --network none --name uws-golang-check \
	--hostname go-check.uws.local -u uws \
	-v ${TMPDIR}:/go/tmp \
	-v ${PWD}/go:/go/src/uws \
	-v ${BUILD_CACHE}:/go/.cache \
	--entrypoint /go/src/uws/check.sh \
	uws/golang-2109
