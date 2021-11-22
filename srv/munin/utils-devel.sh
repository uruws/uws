#!/bin/sh
set -eu

TMPDIR=${PWD}/tmp/munin
mkdir -vp -m 0750 ${TMPDIR}

docker run -it --rm --name uws-munin-devel \
	--hostname munin.uws.local \
	--read-only \
	--workdir /home/uws \
	-v ${PWD}/srv/munin/utils:/home/uws/utils:ro \
	-v ${TMPDIR}:/home/uws/tmp \
	uws/python-2109

exit 0
