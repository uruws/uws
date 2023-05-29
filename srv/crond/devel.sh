#!/bin/sh
set -eu
CA=${PWD}/secret/ca/uws/smtps/230503
mkdir -vp ${PWD}/tmp
exec docker run -it --rm --name uws-crond-devel \
	--hostname crond-devel.uws.local \
	--read-only \
	-u uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	-e USER=uws \
	-e HOME=/home/uws \
	-v ${CA}:/srv/etc/ca:ro \
	-v ${PWD}/tmp:/home/uws/tmp \
	--workdir /home/uws \
	uws/crond-2305
