#!/bin/sh
set -eu
exec docker run -it --rm --name uws-nginx \
	--hostname nginx.uws.local \
	--read-only \
	--tmpfs /run \
	--tmpfs /tmp \
	--tmpfs /var/lib/nginx \
	--tmpfs /var/log/nginx \
	-p 127.0.0.1:0:80 \
	-p 127.0.0.1:0:443 \
	uws/nginx-2305
