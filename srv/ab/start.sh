#!/bin/sh
set -eu

webapp_env=/srv/uws/deploy/secret/webapp/prod/ab.env
webapp_confd=/srv/uws/deploy/secret/webapp/prod/ab

abench_version=$(cat /srv/uws/deploy/srv/ab/VERSION.prod)

if ! test -d "${webapp_confd}"; then
	echo "${webapp_confd}: abench conf dir not found" >&2
	exit 9
fi

exec docker run --rm --read-only \
	--name uws-abench \
	--hostname abench.uws.local \
	--env-file "${webapp_env}" \
	-p 127.0.0.1:2741:2742 \
	-v "${webapp_confd}:/etc/opt/uws/ab:ro" \
	--tmpfs /tmp \
	"uws/abench-${abench_version}"
