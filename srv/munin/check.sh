#!/bin/sh
set -eu

TMPDIR=${PWD}/tmp/munin
mkdir -vp -m 0750 ${TMPDIR}

docker run --rm --name uws-munin-check \
	--read-only \
	--workdir /home/uws \
	-v ${PWD}/srv/munin/utils:/home/uws/utils:ro \
	-v ${TMPDIR}:/home/uws/tmp \
	uws/python-2109 ./utils/test/coverage.sh

exit 0
