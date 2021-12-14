#!/bin/sh
exec docker run -it --rm --network none --name uws-base-testing \
	--hostname base-testing.uws.local -u uws uws/base-testing "$@"
