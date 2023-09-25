#!/bin/sh
set -eu
DATA=${HOME}/uws/munin
mkdir -vp ${DATA}/cache/www
exec docker run -it --rm --name uws-munin-backend \
	--hostname munin-backend.uws.local \
	-v "${DATA}/cache/www:/var/cache/munin/www:ro" \
	-p 127.0.0.1:8049:80 \
	--entrypoint /bin/bash \
	-u root uws/munin-backend-2309
