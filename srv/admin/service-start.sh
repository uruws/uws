#!/bin/sh
set -eu

admin_env=${1:?'admin env?'}

webapp_env="/srv/run/webapp/${admin_env}/admin.env"
webapp_confd="/srv/run/webapp/${admin_env}/admin"
webapp_datad="/srv/run/webapp/${admin_env}/admin.data"

admin_version=$(cat "/srv/run/webapp/${admin_env}/admin.VERSION")

if ! test -d "${webapp_confd}"; then
	echo "${webapp_confd}: uwsadm-${admin_env} conf dir not found" >&2
	exit 9
fi
if ! test -d "${webapp_datad}"; then
	echo "${webapp_datad}: uwsadm-${admin_env} data dir not found" >&2
	exit 8
fi

exec docker run --rm --read-only \
	--name "uwsadm-${admin_env}" \
	--hostname "uwsadm-${admin_env}.uws.local" \
	--env-file "${webapp_env}" \
	-p 127.0.0.1:2743:2741 \
	-v "${webapp_confd}:/etc/opt/uws/admin:ro" \
	-v "${webapp_datad}/uwscli/lib:/srv/home/uwscli/lib:ro" \
	--tmpfs /tmp \
	"uws/admin-${admin_version}"
