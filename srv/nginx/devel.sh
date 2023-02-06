#!/bin/sh
set -eu
exec docker run -it --rm --name uws-nginx-devel \
	--hostname nginx-devel.uws.local \
	--read-only \
	--entrypoint /bin/bash \
	uws/nginx-2211
