#!/bin/sh
set -eu
exec docker run -it --rm --name uws-ab-devel \
	--hostname ab-devel.uws.local \
	--read-only \
	uws/ab-2211
