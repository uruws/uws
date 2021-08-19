#!/bin/sh
set -eu
CANAME="${CANAME:-$(hostname -s)}"
CAVERSION="${CAVERSION:-$(date '+%y%m%d')}"
CAROOT="${CAROOT:-${HOME}/.uws/ca}"
if test 'X' = "X${CANAME}"; then
	CANAME='default'
fi
mkdir -v -m 0700 ${CAROOT}/${CANAME}/${CAVERSION} \
	${CAROOT}/${CANAME}/${CAVERSION}/cert \
	${CAROOT}/${CANAME}/${CAVERSION}/client
exec docker run --rm --network none --name uws-mkcert \
	--hostname "${CAVERSION}.${CANAME}.ca.uws.talkingpts.org" \
	-v "${PWD}/docker/mkcert/etc:/usr/local/etc/ssl:ro" \
	-v "${CAROOT}/${CANAME}/${CAVERSION}:/home/uws/ca" \
	-u uws uws/mkcert "$@"
