#!/bin/sh
set -eu

CLI_HOME=${PWD}/host/assets/jsbatch/srv/home/uwscli

mkdir -vp ${PWD}/tmp/uwscli

exec docker run --rm --name uwscli \
	--hostname cli.uws.local \
	-e PYTHONPATH=/srv/home/uwscli/lib \
	-v ${CLI_HOME}/bin:/srv/home/uwscli/bin:ro \
	-v ${CLI_HOME}/etc:/srv/home/uwscli/etc:ro \
	-v ${CLI_HOME}/lib:/srv/home/uwscli/lib:ro \
	-v ${PWD}/cli:/srv/uws/deploy/cli:ro \
	-v ${PWD}/cli/test:/home/uws/test:ro \
	-v ${PWD}/tmp/uwscli:/home/uws/tmp:rw \
	uws/cli $@
