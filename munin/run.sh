#!/bin/sh
set -eu
mkdir -vp ${PWD}/munin/files
exec docker run -it --rm --name uws-munin \
	--hostname munin.uws.local \
	-v ${PWD}/munin/files:/home/uws/files \
	-u root uws/munin
