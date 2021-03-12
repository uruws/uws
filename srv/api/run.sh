#!/bin/sh
set -eu
HRKDIR=${HOME}/uws/heroku/staging
mkdir -vp ${HRKDIR}
exec docker run --rm --name uws-meteor \
	--hostname meteor.uws.local \
	-v "${HRKDIR}:/home/uws/meteor:ro" \
	-p 127.0.0.1:4080:4080 \
	-u uws uws/api
