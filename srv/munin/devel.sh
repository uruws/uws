#!/bin/sh
set -eu
mkdir -vp ${PWD}/tmp
exec docker run -it --rm --name uws-munin-devel \
	--hostname munin-devel.uws.local \
	--read-only \
	-v ${PWD}/srv/munin:/home/uws/srv/munin:ro \
	-v ${PWD}/tmp:/home/uws/tmp \
	-u uws --entrypoint /usr/local/bin/uws-login.sh \
	-e USER=uws -e HOME=/home/uws \
	--workdir /home/uws \
	--tmpfs /var/local/munin-alert \
	$@ uws/munin
