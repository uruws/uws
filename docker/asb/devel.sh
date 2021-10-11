#!/bin/sh
set -eu
TMPDIR=${PWD}/tmp
mkdir -vp ${TMPDIR}
exec docker run -it --rm --name uws-ansible-devel \
	--hostname ansible-devel.uws.local -u uws \
	--read-only \
	-v ${TMPDIR}:/home/uws/tmp \
	-v ${PWD}/asb:/home/uws/asb:ro \
	--tmpfs /home/uws/.ansible/tmp:rw,mode=1777 \
	uws/ansible
