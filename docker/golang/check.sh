#!/bin/sh
set -eu
BUILD_CACHE=${PWD}/docker/golang/build/cache
BUILD_TMP=${PWD}/docker/golang/tmp
TMPDIR=${PWD}/tmp
mkdir -vp ${BUILD_CACHE} ${TMPDIR} ${BUILD_TMP}
exec docker run --rm --network none --name uws-golang-check \
	--hostname go-check.uws.local -u uws \
	--read-only \
	-v ${PWD}/go:/go/src/uws:ro \
	-v ${BUILD_CACHE}:/go/.cache \
	-v ${BUILD_TMP}:/tmp \
	-v ${TMPDIR}:/go/tmp \
	-e CGO_ENABLED=0 \
	--entrypoint /go/src/uws/check.sh \
	uws/golang-2305
