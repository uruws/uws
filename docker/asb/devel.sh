#!/bin/sh
set -eu

run_args=${DOCKER_RUN_ARGS:-"-it"}

TMPDIR=${PWD}/tmp/ansible
install -v -d -m 0750 ${TMPDIR}
install -v -d -m 0750 ${TMPDIR}/.cache

exec docker run ${run_args} --rm --name uws-ansible-devel \
	--hostname asbdev.ansible.uws.local -u uws \
	--read-only \
	-v ${TMPDIR}:/home/uws/tmp \
	-v ${TMPDIR}/.cache:/home/uws/.cache \
	-v ${PWD}/asb:/home/uws/asb:ro \
	-v ${PWD}/secret/asb:/home/uws/secret:ro \
	--tmpfs /tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/cp:rw,mode=1777 \
	uws/ansible:devel "$@"
