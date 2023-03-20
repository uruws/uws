#!/bin/sh
set -eu

/usr/bin/docker run --rm -u root \
	--name uws-munin-backend-service \
	--hostname munin-backend.uws.local \
	-p 127.0.0.1:8049:80 \
	-v /srv/munin/var/lib:/var/lib/munin:ro \
	-v /srv/munin/var/lib/cgi-tmp:/var/lib/munin/cgi-tmp \
	-v /srv/munin/cache/www:/var/cache/munin/www:ro \
	uws/munin-backend-2211

exit 0
