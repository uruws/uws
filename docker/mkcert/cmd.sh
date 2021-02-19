#!/bin/sh
CAHOST="$(hostname -s)"
CAROOT="${CAROOT:-${HOME}/.uws/ca}"
if test 'X' = "X${CAHOST}"; then
	CAHOST='uwsca'
else
	CAHOST="${CAHOST}.uwsca"
fi
exec docker run --rm --network none --name uws-mkcert \
	--hostname "${CAHOST}.talkingpts.org" \
	-v "${CAROOT}:/home/uws/ca" \
	-u uws uws/mkcert "$@"
