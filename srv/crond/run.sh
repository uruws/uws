#!/bin/sh
set -eu
CA=smtps/230503
CADIR=${PWD}/secret/ca/uws/${CA}
exec docker run -it --rm --name uws-crond \
	--hostname crond.uws.local \
	-v "${CADIR}:/srv/mailx/setup/ca:ro" \
	-v "${CADIR}/client:/srv/mailx/setup/ca.client:ro" \
	uws/crond-2309
