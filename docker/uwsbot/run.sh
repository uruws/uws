#!/bin/sh
set -eu
SRCDIR=${UWS_SRCDIR:-'/srv/deploy/monbots'}
if ! test -d "${SRCDIR}"; then
	echo "${SRCDIR}: dir not found" >&2
	exit 1
fi
exec docker run --rm --name uws-uwsbot \
	--hostname uwsbot.uws.local \
	-v ${SRCDIR}:/uws/share/uwsbot:ro \
	-u uws uws/uwsbot $@
