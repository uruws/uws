#!/bin/sh
set -eu

/usr/bin/docker run --rm -u root \
	--name uws-munin-service \
	--hostname munin.uws.local \
	--add-host docker.uws.local:$(/uws/docker-hostip.sh) \
	-v /srv/munin/var/lib:/var/lib/munin \
	-v /srv/munin/cache/www:/var/cache/munin/www \
	-v /srv/munin/var/log:/var/log/munin \
	-v /srv/etc/munin:/srv/etc/munin \
	789470191893.dkr.ecr.us-east-1.amazonaws.com/uws:munin

exit 0
