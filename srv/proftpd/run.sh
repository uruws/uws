#!/bin/sh
set -eu
mkdir -vp /srv/uws/sftp/run /srv/uws/sftp/home
exec docker run -it --rm --name uws-proftpd \
	--hostname proftpd.uws.local \
	--read-only \
	-p 127.0.0.1:2222:22 \
	-v /srv/uws/sftp/run:/run \
	-v /srv/uws/sftp/home:/srv/ftp \
	uws/proftpd
