#!/bin/sh
set -eu
BOT_ENV=${1:-'default'}
BOT_NAME=${2:-'default'}
SRCDIR=${UWS_SRCDIR:-'/srv/deploy/monbots'}
if ! test -d "${SRCDIR}"; then
	echo "${SRCDIR}: dir not found" >&2
	exit 1
fi
CFGDIR=${UWS_CFGDIR:-"${HOME}/.uws/bot/${BOT_ENV}/${BOT_NAME}"}
STATSDIR=${UWS_STATSDIR:-'/srv/uwsbot/stats'}
STATSDIR="${STATSDIR}/${BOT_ENV}"
SECDIR=${UWS_SECDIR:-'/srv/uwsbot/sec'}
SECDIR="${SECDIR}/${BOT_ENV}"
mkdir -vp "${CFGDIR}" "${STATSDIR}"
exec docker run --rm --name "uws-bot-${BOT_ENV}-${BOT_NAME}" \
	--hostname "bot-${BOT_ENV}-${BOT_NAME}.uws.local" \
	-v "${SRCDIR}:/uws/share/uwsbot:ro" \
	-v "${CFGDIR}:/home/uws/.config/uws/bot:ro" \
	-v "${STATSDIR}:/uws/var/uwsbot/stats" \
	-v "${SECDIR}/bot:/uws/etc/sec/bot" \
	-e "UWS_LOG=quiet" \
	-e "UWS_PREFIX=/uws" \
	-u root uws/uwsbot-2305 -env "${BOT_ENV}" -name "${BOT_NAME}"
