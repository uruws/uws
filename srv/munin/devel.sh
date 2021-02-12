#!/bin/sh
set -eu
exec docker run -it --rm --name uws-munin-devel \
	--hostname munin-devel.uws.local \
	-v ${PWD}/srv/munin:/home/uws/srv/munin \
	-u uws --entrypoint /bin/bash \
	-e USER=uws -e HOME=/home/uws \
	--workdir /home/uws \
	$@ uws/munin
