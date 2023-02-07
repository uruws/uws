#!/bin/sh
set -eu
exec docker run -it --rm --name uws-nginx-devel \
	--hostname nginx-devel.uws.local \
	--read-only \
	--entrypoint /bin/bash \
	--tmpfs /run \
	--tmpfs /tmp \
	--tmpfs /var/lib/nginx \
	--tmpfs /var/log/nginx \
	-v ${PWD}/srv/nginx/utils:/usr/local/bin:ro \
	-v ${PWD}/srv/nginx/etc/conf.d:/etc/nginx/conf.d:ro \
	uws/nginx-2211
