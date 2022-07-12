#!/bin/sh
set -eu
cd /srv/uws/deploy
logfn=/srv/uwscli/logs/prod-setup.log

date -R | tee "${logfn}"
./cli/schroot/setup.sh prod 2>&1 | tee -a "${logfn}"
date -R | tee -a "${logfn}"

if ! systemctl is-enabled uwscli-@prod.service; then
	systemctl enable uwscli-@prod.service 2>&1 | tee -a "${logfn}"
	systemctl start uwscli-@prod.service 2>&1 | tee -a "${logfn}"
fi

export DOCKER_IMAGE='uws/cli-2203'

/uws/bin/service-restart.sh uwscli-@prod \
	/etc/systemd/system/uwscli-@.service \
	/srv/uwscli/prod/secret \
	/srv/uwscli/schroot/start.sh \
	/srv/uwscli/schroot/stop.sh \
	2>&1 | tee -a "${logfn}"

exit 0
