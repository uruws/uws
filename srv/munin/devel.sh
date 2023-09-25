#!/bin/sh
set -eu
mkdir -vp ${PWD}/tmp
exec docker run -it --rm --name uws-munin-devel \
	--hostname munin-devel.uws.local \
	--read-only \
	-u uws --entrypoint /usr/local/bin/uws-login.sh \
	-e USER=uws -e HOME=/home/uws \
	-v ${PWD}/srv/munin/utils:/opt/munin \
	-v ${PWD}/tmp:/home/uws/tmp \
	-v ${PWD}/python:/opt/uws \
	--tmpfs /tmp \
	--tmpfs /var/opt/munin-alert \
	--workdir /opt/munin \
	$@ uws/munin-2309
