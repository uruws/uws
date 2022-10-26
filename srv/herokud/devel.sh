#!/bin/sh
set -eu
CA=${PWD}/secret/ca/uws/smtps/211006
mkdir -vp ${PWD}/tmp
exec docker run -it --rm --name uws-herokud-devel \
	--hostname herokud-devel.uws.local \
	--read-only \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	--workdir /home/uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	-v ${CA}:/srv/etc/ca:ro \
	-v ${PWD}/tmp:/home/uws/tmp \
	--tmpfs /home/uws/.cache/heroku \
	--tmpfs /run \
	--tmpfs /tmp \
	uws/herokud
