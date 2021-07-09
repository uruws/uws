#!/bin/sh
set -eu
exec docker run -it --rm --name uws-proftpd \
	--hostname proftpd.uws.local \
	--read-only \
	--tmpfs /run:rw,size=100m,mode=1777 \
	-p 127.0.0.1:2222:22 \
	uws/proftpd
