#!/bin/sh
set -eu
HRKDIR=${HOME}/uws/heroku/staging
mkdir -vp ${HRKDIR}
exec docker run --rm --name uws-api \
	--hostname api.uws.local \
	-v "${HRKDIR}:/home/uws/api:ro" \
	-u uws uws/api
