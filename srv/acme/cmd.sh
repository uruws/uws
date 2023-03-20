#!/bin/sh
set -eu
ACME_HOME=${ACME_HOME:-${HOME}/uws/acme}
ACME_RUN=${ACME_RUN:-${HOME}/uws/acme.run}
umask 0027
mkdir -vp ${ACME_HOME} ${ACME_RUN}
exec docker run --rm --name uws-acme-cmd \
	--hostname acme-cmd.uws.local \
	-v ${ACME_HOME}:/srv/acme \
	-v ${ACME_RUN}:/srv/run/acme \
	-u uws uws/acme-2211 $@
