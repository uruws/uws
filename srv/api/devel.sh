#!/bin/sh
set -eu
HRKDIR=${HOME}/uws/heroku/staging
mkdir -vp ${HRKDIR}
exec docker run -it --rm --name uws-api-devel \
	--hostname api-devel.uws.local \
	-v ${HRKDIR}:/home/uws/api \
	-u uws uws/api
