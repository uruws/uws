#!/bin/sh
set -eu
BOT_NAME=${1:-'default'}
BOT_ENV=${2:-'default'}
SRCDIR=${UWS_SRCDIR:-'/srv/deploy/monbots'}
if ! test -d "${SRCDIR}"; then
	echo "${SRCDIR}: dir not found" >&2
	exit 1
fi
CFGDIR=${UWS_CFGDIR:-"${HOME}/.uws/bot/${BOT_ENV}/${BOT_NAME}"}
mkdir -vp ${CFGDIR}
exec docker run --rm --name "uws-bot-${BOT_ENV}-${BOT_NAME}" \
	--hostname "bot-${BOT_ENV}-${BOT_NAME}.uws.local" \
	-v "${SRCDIR}:/uws/share/uwsbot:ro" \
	-v "${CFGDIR}:/home/uws/.config/uws/bot:ro" \
	-u uws uws/uwsbot -env "bot/${BOT_ENV}" -name "${BOT_NAME}"
