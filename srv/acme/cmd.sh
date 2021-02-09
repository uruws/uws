#!/bin/sh
set -eu
ACME_HOME=${ACME_HOME:-${HOME}/uws/acme}
umask 0027
mkdir -vp ${ACME_HOME}
exec docker run --rm --name uws-acme-cmd \
	--hostname acme-cmd.uws.local \
	-v ${ACME_HOME}:/srv/acme \
	-u uws uws/acme $@
