#!/bin/sh
set -eu

TMPDIR=${PWD}/tmp/munin-node
mkdir -vp -m 0750 ${TMPDIR}

docker run --rm --name uws-munin-node-check \
	--hostname munin-node.uws.local \
	--read-only \
	--workdir /home/uws \
	-v ${PWD}/srv/munin-node/utils:/home/uws/utils:ro \
	-v ${PWD}/srv/munin-node/test:/home/uws/test:ro \
	-v ${TMPDIR}:/home/uws/tmp \
	uws/python-2109 $@

exit 0
