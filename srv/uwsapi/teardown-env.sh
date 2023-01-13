#!/bin/sh
set -u

envname="${1:?'env name?'}"

if systemctl is-enabled "uwsapi-@${envname}.service"; then
	systemctl stop "uwsapi-@${envname}.service"
	sleep 1
	systemctl disable "uwsapi-@${envname}.service"
	rm -vf /etc/systemd/system/uwsapi-@.service
	systemctl daemon-reload
fi

exit 0
