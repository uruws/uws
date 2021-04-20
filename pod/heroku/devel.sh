#!/bin/sh
set -eu
HRKDIR=${HOME}/uws/heroku/staging
mkdir -vp ${HRKDIR}
exec docker run -it --rm --name uws-meteor-devel \
	--hostname meteor-devel.uws.local \
	-v "${HRKDIR}:/home/uws/meteor:ro" \
	--entrypoint /usr/local/bin/uws-login.sh \
	-u uws uws/api
