#!/bin/sh
set -eu

webapp_env=/srv/run/webapp/prod/ab.env
webapp_confd=/srv/run/webapp/prod/ab
webapp_datad=/srv/run/webapp/prod/ab/data

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
	-v "${webapp_datad}:/var/lib/abench" \
	--tmpfs /tmp \
	"uws/abench-${abench_version}"
