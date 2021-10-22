#!/bin/sh
set -eu
ACME_HOME=/srv/acme
ACME_RUN=/srv/run/acme
mkdir -vp ${ACME_HOME} ${ACME_RUN}
exec docker run --rm --name uws-acme-cmd \
	--hostname acme-cmd.uws.local \
	-v ${ACME_HOME}:/srv/acme \
	-v ${ACME_RUN}:/srv/run/acme \
	--workdir /home/uwsops \
	-e USER=uwsops \
	-e HOME=/home/uwsops \
	-u uwsops uwsops/acme $@
