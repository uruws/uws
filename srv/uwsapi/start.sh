#!/bin/sh
set -eu
envname="${1:?'env name?'}"
umask 0027
port=3800
if test "X${envname}" = 'Xtest'; then
	port=3810
fi
exec docker run --rm --name "uwsapi-${envname}" \
	--hostname "api${envname}.uws.local" \
	--read-only \
	-p "127.0.0.1:${port}:3800" \
	uws/api-2203
