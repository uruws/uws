#!/bin/sh
set -eu
exec docker run --rm --name uws-nginx-check \
	--hostname nginx-check.uws.local \
	--read-only \
	--entrypoint /root/test/check.sh \
	--tmpfs /run \
	--tmpfs /tmp \
	--tmpfs /var/lib/nginx \
	--tmpfs /var/log/nginx \
	--tmpfs /etc/nginx/uws-sites-enabled \
	-v ${PWD}/srv/nginx/test:/root/test:ro \
	uws/nginx-2305
