#!/bin/sh
set -eu

admin_env=${1:?'admin env?'}

if ! systemctl is-enabled "uwsadm-${admin_env}.service"; then
	systemctl enable "uwsadm-${admin_env}.service"
	systemctl start "uwsadm-${admin_env}"
fi

install -v -d -m 0755 -o root -g uws "/srv/run/webapp/${admin_env}/admin"

install -v -m 0755 -o root -g uws \
	"/srv/uws/deploy/srv/admin/service-start.sh" \
	"/srv/run/webapp/${admin_env}/admin-service-start.sh"

install -v -m 0755 -o root -g uws \
	"/srv/uws/deploy/srv/admin/service-stop.sh" \
	"/srv/run/webapp/${admin_env}/admin-service-stop.sh"

install -v -m 0644 -o root -g uws \
	"/srv/uws/deploy/srv/admin/VERSION.${admin_env}" \
	"/srv/run/webapp/${admin_env}/admin.VERSION"

install -v -m 0644 -o root -g uws \
	"/srv/uws/deploy/secret/webapp/${admin_env}/admin.env" \
	"/srv/run/webapp/${admin_env}/admin.env"

install -v -m 0644 -o root -g uws \
	"/srv/uws/deploy/secret/webapp/${admin_env}/admin/admin_conf.py" \
	"/srv/run/webapp/${admin_env}/admin/admin_conf.py"

install -v -d -m 1777 -o root -g root "/srv/run/webapp/${admin_env}/admin/data"

admin_version=$(cat "/srv/run/webapp/${admin_env}/admin.VERSION")
export DOCKER_IMAGE="uws/admin-${admin_version}"

/uws/bin/service-restart.sh "uwsadm-${admin_env}" \
	"/srv/run/webapp/${admin_env}/admin.env" \
	"/srv/run/webapp/${admin_env}/admin/admin_conf.py" \
	"/srv/run/webapp/${admin_env}/admin.VERSION" \
	"/srv/run/webapp/${admin_env}/admin-service-stop.sh" \
	"/srv/run/webapp/${admin_env}/admin-service-start.sh"

exit 0
