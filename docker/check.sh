#!/bin/sh
set -eu

TMPDIR=${PWD}/tmp
install -v -d -m 0750 ${TMPDIR}

exec docker run --rm --name uws-docker-devel \
	--hostname dockerdev.ansible.uws.local -u uws \
	--read-only \
	-v ${TMPDIR}:/home/uws/tmp \
	-v ${PWD}/docker:/home/uws/docker:ro \
	--workdir /home/uws/docker \
	uws/python-2309 "$@"
