#!/bin/sh
CAROOT=${CAROOT:-${HOME}/.uws/ca}
mkdir -vp ${CAROOT}
exec docker run --rm --name uws-mkcert \
	--hostname mkcert.uws.local \
	-v ${CAROOT}:/home/uws/ca \
	-u uws uws/mkcert $@
