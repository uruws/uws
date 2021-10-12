#!/bin/sh
set -eu
TMPDIR=${PWD}/tmp
mkdir -vp ${TMPDIR}
exec docker run -it --rm --name uws-ansible-devel \
	--hostname ansible-devel.uws.local -u uws \
	--read-only \
	-e AWS_PROFILE=uwsasb \
	-e AWS_REGION=sa-east-1 \
	-e ANSIBLE_CONFIG=/home/uws/asb/ansible.cfg \
	-v ${TMPDIR}:/home/uws/tmp \
	-v ${PWD}/asb:/home/uws/asb:ro \
	-v ${PWD}/secret/asb/aws:/home/uws/.aws:ro \
	--tmpfs /tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/tmp:rw,mode=1777 \
	--tmpfs /home/uws/.ansible/cp:rw,mode=1777 \
	uws/ansible
