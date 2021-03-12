#!/bin/sh
set -eu
HRKDIR=${HOME}/uws/heroku/staging
mkdir -vp ${HRKDIR}
exec docker run --rm --name uws-meteor \
	--hostname meteor.uws.local \
	-v "${HRKDIR}:/home/uws/meteor:ro" \
	--log-driver syslog \
	-u uws uws/api
