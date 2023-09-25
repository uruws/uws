#!/bin/sh
set -eu
DATA=${HOME}/uws/munin
mkdir -vp ${DATA}/var/lib ${DATA}/cache/www ${DATA}/var/log
exec docker run -it --rm --name uws-munin \
	--hostname munin.uws.local \
	-v ${DATA}/var/lib:/var/lib/munin \
	-v ${DATA}/cache/www:/var/cache/munin/www \
	-v ${DATA}/var/log:/var/log/munin \
	-u root uws/munin-2309
