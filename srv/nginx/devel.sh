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
	--tmpfs /etc/nginx/uws-sites-enabled \
	-v ${PWD}/srv/nginx/utils:/usr/local/bin:ro \
	-v ${PWD}/srv/nginx/etc/conf.d:/etc/nginx/conf.d:ro \
	-v ${PWD}/srv/nginx/etc/snippets:/etc/nginx/snippets:ro \
	-v ${PWD}/srv/nginx/etc/sites-enabled:/etc/nginx/sites-enabled:ro \
	-v ${PWD}/srv/nginx/test:/root/test:ro \
	-p 127.0.0.1:0:80 \
	-p 127.0.0.1:0:443 \
	uws/nginx-2211
