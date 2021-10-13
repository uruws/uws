#!/bin/sh
set -eu

asbenv=${1:?'ansible env?'}
envfn=${PWD}/asb/env/${asbenv}.env

TMPDIR=${PWD}/tmp
mkdir -vp ${TMPDIR}

exec docker run -it --rm --name uws-ansible-devel \
	--hostname ansible-devel.uws.local -u uws \
	--read-only \
	--env-file ${envfn} \
	-v ${TMPDIR}:/home/uws/tmp \
	-v ${PWD}/asb:/home/uws/asb:ro \
	-v ${PWD}/secret/asb:/home/uws/secret:ro \
	-v ${PWD}/secret/asb/aws:/home/uws/.aws:ro \
	--tmpfs /tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/cp:rw,mode=1777 \
	uws/ansible
