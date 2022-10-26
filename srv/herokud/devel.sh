#!/bin/sh
set -eu
CA=${PWD}/secret/ca/uws/smtps/211006
mkdir -vp ${PWD}/tmp
exec docker run -it --rm --name uws-herokud-devel \
	--hostname herokud-devel.uws.local \
	--read-only \
	--entrypoint /usr/local/bin/uws-login.sh \
	-v ${CA}:/srv/etc/ca:ro \
	-v ${PWD}/tmp:/home/uws/tmp \
	--workdir /home/uws \
	uws/herokud
