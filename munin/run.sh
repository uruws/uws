#!/bin/sh
set -eu
mkdir -vp ${PWD}/munin/files
mkdir -vp ~/uws/munin/var ~/uws/munin/cache ~/uws/munin/log
exec docker run -it --rm --name uws-munin \
	--hostname munin.uws.local \
	-v ${PWD}/munin/files:/home/uws/files \
	-v ~/uws/munin/var:/var/lib/munin \
	-v ~/uws/munin/cache:/var/cache/munin/www \
	-v ~/uws/munin/log:/var/log/munin \
	-u root uws/munin
