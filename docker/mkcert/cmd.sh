#!/bin/sh
set -eu
CANAME="${CANAME:-$(hostname -s)}"
CAVERSION="${CAVERSION:-$(date '+%y%m%d')}"
CAROOT="${CAROOT:-${HOME}/.uws/ca}"
if test 'X' = "X${CANAME}"; then
	CANAME='default'
fi
CADIR=${CAROOT}/${CANAME}/${CAVERSION}
install -d -m 0700 ${CAROOT}/${CANAME}/etc \
	${CADIR} ${CADIR}/cert ${CADIR}/client ${CADIR}/revoke
exec docker run --rm --network none --name uws-mkcert \
	--hostname "${CAVERSION}.${CANAME}.ca.uws.talkingpts.org" \
	-v "${PWD}/docker/mkcert/etc:/usr/local/etc/ssl:ro" \
	-v "${CAROOT}/${CANAME}/etc:/usr/local/etc/ca:ro" \
	-v "${CADIR}:/home/uws/ca" \
	-u uws uws/mkcert-2211 "$@"
