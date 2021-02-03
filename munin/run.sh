#!/bin/sh
set -eu
mkdir -vp ${PWD}/munin/files
mkdir -vp ~/uws/munin/var/lib ~/uws/munin/cache/www
exec docker run -it --rm --name uws-munin \
	--hostname munin.uws.local \
	-v ${PWD}/munin/files:/home/uws/files \
	-v ~/uws/munin/var/lib:/var/lib/munin \
	-v ~/uws/munin/cache/www:/var/cache/munin/www \
	-u root uws/munin
