#!/bin/sh
set -eu
CA=smtps/230503
CADIR=${PWD}/secret/ca/uws/${CA}
mkdir -vp ${PWD}/tmp/crond
exec docker run -it --rm --name uws-crond-devel \
	--hostname crond-devel.uws.local \
	--read-only \
	-u uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	-e USER=uws \
	-e HOME=/home/uws \
	-v "${CADIR}:/srv/mailx/setup/ca:ro" \
	-v "${CADIR}/client:/srv/mailx/setup/ca.client:ro" \
	-v "${PWD}/tmp/crond:/home/uws/tmp" \
	--workdir /home/uws \
	uws/crond-2309
