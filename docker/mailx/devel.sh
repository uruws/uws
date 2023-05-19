#!/bin/sh
set -eu
CA=${PWD}/secret/ca/uws/smtps/230503
mkdir -vp ${PWD}/tmp
exec docker run -it --rm --name uws-mailx-devel \
	--hostname mailx-devel.uws.local \
	--read-only \
	-u uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	-e USER=uws \
	-e HOME=/home/uws \
	-v ${PWD}/tmp:/home/uws/tmp \
	-v ${CA}:/srv/etc/ca:ro \
	--tmpfs /tmp \
	--workdir /home/uws \
	uws/mailx-2305
