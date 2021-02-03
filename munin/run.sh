#!/bin/sh
set -eu
mkdir -vp ${PWD}/munin/files
mkdir -vp ~/uws/munin/var/lib ~/uws/munin/cache/www ~/uws/munin/var/log
exec docker run -it --rm --name uws-munin \
	--hostname munin.uws.local \
	-v ~/uws/munin/var/lib:/var/lib/munin \
	-v ~/uws/munin/cache/www:/var/cache/munin/www \
	-v ~/uws/munin/var/log:/var/log/munin \
	-u root uws/munin
