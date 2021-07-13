#!/bin/sh
set -eu
sftp_home=${SFTP_HOME:-'/srv/uws/sftp/home'}
sftp_addr=${SFTP_ADDR:-'127.0.0.1'}
sftp_port=${SFTP_PORT:-'2222'}
mkdir -vp ${sftp_home}
exec docker run -it --rm --name uws-proftpd \
	--hostname proftpd.uws.local \
	--read-only -u root \
	-p "${sftp_addr}:${sftp_port}:22" \
	-v "${sftp_home}:/srv/ftp" \
	--tmpfs /run:rw,mode=1777,size=10m \
	uws/proftpd
