#!/bin/sh
set -eu
ACME_HOME=/srv/acme
ACME_RUN=/srv/run/acme
ACME_IMG=789470191893.dkr.ecr.sa-east-1.amazonaws.com/uwsops:acme
mkdir -vp ${ACME_HOME} ${ACME_RUN}
exec docker run --rm --name uws-acme-cmd \
	--hostname acme-cmd.uws.local \
	-v ${ACME_HOME}:/srv/acme \
	-v ${ACME_RUN}:/srv/run/acme \
	-u uws ${ACME_IMG} $@
