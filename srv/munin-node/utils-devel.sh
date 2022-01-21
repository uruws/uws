#!/bin/sh
set -eu

TMPDIR=${PWD}/tmp/munin-node
mkdir -vp -m 0750 ${TMPDIR}

docker run -it --rm --name uws-munin-node-utils-devel \
	--hostname munin-node.uws.local \
	--read-only \
	--workdir /home/uws \
	-e PYTHONPATH=/uws/lib/plugins \
	-v ${PWD}/srv/munin-node/utils:/home/uws/utils:ro \
	-v ${PWD}/srv/munin-node/test:/home/uws/test:ro \
	-v ${PWD}/srv/munin-node/plugins/bin:/uws/bin \
	-v ${PWD}/srv/munin-node/plugins/lib:/uws/lib/plugins \
	-v ${TMPDIR}:/home/uws/tmp \
	uws/python-2109

exit 0
