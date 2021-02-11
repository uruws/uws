#!/bin/sh
set -eu

SERVICE=${1:?'service name?'}
shift
CHECK="$@"

if test "X${CHECK}" = 'X'; then
	echo "ERROR - service restart ${SERVICE} no files to check" >&2
	exit 1
fi

lastfn=/srv/run/uws-service-restart.${SERVICE}
if ! test -s ${lastfn}; then
	echo 'NONE' >${lastfn}
fi
LAST="$(cat ${lastfn})"

cksum() {
	find ${CHECK} -type f 2>/dev/null | xargs sha256sum | sha256sum - | cut -d ' ' -f 1
}
CUR="$(cksum)"

if test "X${CUR}" != "X${LAST}"; then
	echo "i - restart service: ${SERVICE}"
	service ${SERVICE} restart
fi

exit 0
