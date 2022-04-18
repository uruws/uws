#!/bin/sh
set -eu
envname="${1:?'env name?'}"
umask 0027
exec docker run -it --rm --name "uwsapi-${envname}" \
	--hostname "api${envname}.uws.local" \
	--read-only \
	-p 127.0.0.1:3800:3800 \
	uws/api-2203
