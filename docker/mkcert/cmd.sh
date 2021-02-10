#!/bin/sh
CAROOT=${CAROOT:-${HOME}/.uws/ca}
mkdir -vp ${CAROOT}
exec docker run --rm --network none --name uws-mkcert \
	--hostname uwsca.talkingpts.org \
	-v ${CAROOT}:/home/uws/ca \
	-u uws uws/mkcert $@
