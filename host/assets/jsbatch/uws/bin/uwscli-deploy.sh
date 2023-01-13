#!/bin/sh
set -eu
cd /srv/uws/deploy
logfn=/srv/uwscli/logs/prod-setup.log

date -R | tee "${logfn}"
./cli/schroot/setup.sh prod 2>&1 | tee -a "${logfn}"
date -R | tee -a "${logfn}"

surun='sudo -n'

if ! ${surun} systemctl is-enabled uwscli-@prod.service; then
	${surun} systemctl enable uwscli-@prod.service 2>&1 | tee -a "${logfn}"
	${surun} systemctl start uwscli-@prod.service 2>&1 | tee -a "${logfn}"
	exit 0
fi

export DOCKER_IMAGE='uws/cli-2211'

${surun} /uws/bin/service-restart.sh uwscli-@prod \
	/etc/systemd/system/uwscli-@.service \
	/srv/uwscli/prod/secret \
	/srv/uwscli/schroot/start.sh \
	/srv/uwscli/schroot/stop.sh \
	2>&1 | tee -a "${logfn}"

exit 0
