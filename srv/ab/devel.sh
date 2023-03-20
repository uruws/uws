#!/bin/sh
set -eu
exec docker run -it --rm --name uws-ab-devel \
	--hostname ab-devel.uws.local \
	--read-only \
	--entrypoint /usr/local/bin/uws-login.sh \
	uws/ab-2211
