#!/bin/sh
set -eu

SECRET=${PWD}/secret/eks/files/munin

TMPDIR=${PWD}/tmp/munin
mkdir -vp -m 0750 ${TMPDIR}

RUN='shellcheck.sh coverage.sh'

for cmd in $(echo ${RUN}); do
	echo "***** munin/utils/test/${cmd}"
	docker run --rm --name uws-munin-check \
		--read-only \
		--workdir /home/uws \
		-v ${PWD}/srv/munin/utils:/home/uws/utils:ro \
		-v ${SECRET}:/home/uws/secret:ro \
		-v ${TMPDIR}:/home/uws/tmp \
		uws/python-2305 ./utils/test/${cmd}
done

exit 0
