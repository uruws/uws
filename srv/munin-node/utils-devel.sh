#!/bin/sh
set -eu

TMPDIR=${PWD}/tmp/munin-node
mkdir -vp -m 0750 ${TMPDIR} ${TMPDIR}/etc
mkdir -vp -m 0750 ${TMPDIR}/etc/munin ${TMPDIR}/etc/munin/plugins \
	${TMPDIR}/etc/munin/plugin-conf.d

docker run -it --rm --name uws-munin-node-utils-devel \
	--hostname munin-node.uws.local \
	--read-only \
	--workdir /home/uws \
	-e PYTHONPATH=/uws/lib/plugins \
	-v ${PWD}/srv/munin-node/utils:/home/uws/utils:ro \
	-v ${PWD}/srv/munin-node/test:/home/uws/test:ro \
	-v ${PWD}/srv/munin-node/plugins/bin:/uws/bin:ro \
	-v ${PWD}/srv/munin-node/plugins/lib:/uws/lib/plugins \
	-v ${TMPDIR}:/home/uws/tmp \
	-v ${TMPDIR}/etc/munin:/etc/munin \
	-v ${PWD}/srv/munin-node/test/env:/uws/etc \
	-v ${PWD}/secret/ca/uws/ops/etc:/uws/etc/ca/ops:ro \
	-v ${PWD}/secret/ca/uws/ops/210823/client:/uws/etc/ca/client:ro \
	uws/python-2309

exit 0
