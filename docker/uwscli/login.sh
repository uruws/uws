#!/bin/sh
set -eu

mkdir -vp ${PWD}/tmp/uwscli ${PWD}/tmp/uwscli_rundir
install -v -m 1777 -d ${PWD}/tmp/uwscli_logs

exec docker run -it --rm --name uwscli-login \
	--hostname uwscli.uws.local \
	-v ${PWD}/tmp/uwscli_rundir:/run/uwscli:rw \
	-v ${PWD}/tmp/uwscli_logs:/srv/home/uwscli/logs:rw \
	uws/uwscli-2203 "$@"
