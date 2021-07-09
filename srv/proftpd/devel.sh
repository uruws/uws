#!/bin/sh
set -eu
exec docker run -it --rm --name uws-proftpd-devel \
	--hostname proftpd-devel.uws.local \
	--entrypoint /bin/bash \
	-v ${PWD}/srv/proftpd/config:/mnt/config \
	-v ${PWD}/srv/proftpd/secret/auth:/mnt/auth \
	uws/proftpd
