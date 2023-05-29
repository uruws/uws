#!/bin/sh
set -eu

asbenv=${1:?'ansible env?'}
envfn=${PWD}/asb/env/${asbenv}.env

TMPDIR=${PWD}/tmp
mkdir -vp ${TMPDIR}

exec docker run -it --rm --name uws-ansible-${asbenv} \
	--hostname ${asbenv}.ansible.uws.local -u uws \
	--read-only \
	--env-file ${envfn} \
	-e ASBENV=${asbenv} \
	-e ASBENV_FILENAME=/home/uws/asb/env/${asbenv}.env \
	-v ${TMPDIR}:/home/uws/tmp \
	-v ${PWD}/asb:/home/uws/asb:ro \
	-v ${PWD}/docker/asb/files/ssh:/home/uws/.ssh:ro \
	-v ${PWD}/secret/asb:/home/uws/secret:ro \
	-v ${PWD}/secret/asb/aws:/home/uws/.aws:ro \
	-v ${PWD}/secret/ca/uws:/home/uws/ca:ro \
	-v ${PWD}/srv:/home/uws/srv:ro \
	--tmpfs /tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/cp:rw,mode=1777 \
	uws/ansible-2305
