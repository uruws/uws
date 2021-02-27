#!/bin/sh
set -eu
BOT_NAME=${1:-'default'}
BOT_ENV=${2:-'default'}
SRCDIR=${UWS_SRCDIR:-'/srv/deploy/monbots'}
if ! test -d "${SRCDIR}"; then
	echo "${SRCDIR}: dir not found" >&2
	exit 1
fi
exec docker run --rm --name "uws-uwsbot-${BOT_ENV}-${BOT_NAME}" \
	--hostname "uwsbot-${BOT_ENV}-${BOT_NAME}.uws.local" \
	-v "${SRCDIR}:/uws/share/uwsbot:ro" \
	-u uws uws/uwsbot -env "bot/${BOT_ENV}" -name "${BOT_NAME}"
