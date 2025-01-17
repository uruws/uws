#!/bin/sh
set -eu
exec docker run --rm --name uws-nginx-check \
	--hostname nginx-check.uws.local \
	--read-only \
	--entrypoint /root/test/check.sh \
	--tmpfs /run \
	--tmpfs /tmp \
	--tmpfs /var/cache/nginx \
	--tmpfs /var/cache/nginx.store \
	--tmpfs /var/cache/nginx.temp \
	--tmpfs /var/lib/nginx \
	--tmpfs /var/log/nginx \
	--tmpfs /etc/nginx/uws-sites-enabled \
	-v ${PWD}/srv/nginx/test:/root/test:ro \
	uws/nginx-2309
