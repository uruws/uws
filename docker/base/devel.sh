#!/bin/sh
exec docker run -it --rm --network none --name uws-base \
	--hostname base.uws.local -u uws uws/base-2305 "$@"
