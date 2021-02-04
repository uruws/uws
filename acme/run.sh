#!/bin/sh
set -eu
exec docker run -it --rm --name uws-acme \
	--hostname acme.uws.local \
	-u uws uws/acme $@
