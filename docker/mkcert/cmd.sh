#!/bin/sh
set -eu
CANAME="${CANAME:-$(hostname -s)}"
CAVERSION="${CAVERSION:-$(date '+%y%m%d')}"
CAROOT="${CAROOT:-${HOME}/.uws/ca}"
if test 'X' = "X${CANAME}"; then
	CANAME='default'
fi
exec docker run --rm --network none --name uws-mkcert \
	--hostname "${CAVERSION}.${CANAME}.ca.uws.talkingpts.org" \
	-v "${CAROOT}:/home/uws/ca" \
	-u uws uws/mkcert "$@"
