#!/bin/sh
set -eu
mkdir -vp /srv/uws/sftp/home
exec docker run -it --rm --name uws-proftpd \
	--hostname proftpd.uws.local \
	--read-only -u root \
	-p 127.0.0.1:2222:22 \
	-v /srv/uws/sftp/home:/srv/ftp \
	--tmpfs /run:rw,mode=1777,size=10m \
	uws/proftpd
