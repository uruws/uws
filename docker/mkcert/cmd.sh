#!/bin/sh
CAROOT=${CAROOT:-${HOME}/.uws/ca}
exec docker run --rm --network none --name uws-mkcert \
	--hostname ca.talkingpts.org \
	-v ${CAROOT}:/home/uws/ca \
	-u uws uws/mkcert $@
