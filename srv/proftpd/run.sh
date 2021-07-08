#!/bin/sh
set -eu
exec docker run -it --rm --name uws-proftpd \
	--hostname proftpd.uws.local \
	--read-only \
	--tmpfs /run:rw,size=100m,mode=1777 \
	uws/proftpd
