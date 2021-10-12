#!/bin/sh
set -eu
TMPDIR=${PWD}/tmp
mkdir -vp ${TMPDIR}
exec docker run -it --rm --name uws-ansible-devel \
	--hostname ansible-devel.uws.local -u uws \
	--read-only \
	-e AWS_PROFILE=default \
	-e AWS_REGION=sa-east-1 \
	-v ${TMPDIR}:/home/uws/tmp \
	-v ${PWD}/asb:/home/uws/asb:ro \
	--tmpfs /tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/tmp:rw,mode=1777 \
	uws/ansible
