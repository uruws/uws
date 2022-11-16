#!/bin/sh
exec docker run -it --rm --name uws-mkcert \
	--hostname mkcert.uws.local -u uws uws/mkcert-2211 "$@"
