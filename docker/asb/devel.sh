#!/bin/sh
set -eux

run_args=${DOCKER_RUN_ARGS:-"-it"}

TMPDIR=${PWD}/tmp
install -v -d -m 0750 ${TMPDIR}

exec docker run ${run_args} --rm --name uws-ansible-devel \
	--hostname asbdev.ansible.uws.local -u uws \
	--read-only \
	-v ${TMPDIR}:/home/uws/tmp \
	-v ${PWD}/asb:/home/uws/asb:ro \
	-v ${PWD}/secret/asb:/home/uws/secret:ro \
	-v ${PWD}/secret/ca/uws:/home/uws/ca:ro \
	--tmpfs /tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/cp:rw,mode=1777 \
	uws/ansible
