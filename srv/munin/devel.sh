#!/bin/sh
set -eu
exec docker run -it --rm --name uws-munin-devel \
	--hostname munin-devel.uws.local \
	--read-only \
	-v ${PWD}/srv/munin:/home/uws/srv/munin:ro \
	-u uws --entrypoint /usr/local/bin/uws-login.sh \
	-e USER=uws -e HOME=/home/uws \
	--workdir /home/uws \
	$@ uws/munin
