#!/bin/sh
set -eu
exec docker run -it --rm --name uws-api \
	--hostname api.uws.local \
	--read-only \
	-p 127.0.0.1:3800:3800 \
	--entrypoint /bin/bash \
	uws/api-2203
