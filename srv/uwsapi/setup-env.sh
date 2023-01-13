#!/bin/sh
set -eu

envname="${1:?'env name?'}"

umask 0027

if ! systemctl is-enabled "uwsapi-@${envname}.service"; then
	systemctl enable "uwsapi-@${envname}.service"
	systemctl start "uwsapi-@${envname}.service"
fi

export DOCKER_IMAGE='uwsapp-2203'

/uws/bin/service-restart.sh "uwsapi-@${envname}" \
	/etc/systemd/system/uwsapi-@.service \
	/srv/uwscli/apid/start.sh \
	/srv/uwscli/apid/stop.sh

exit 0
