#!/bin/sh
set -eu

CLI_HOME=${PWD}/host/assets/jsbatch/srv/home/uwscli

exec docker run -it --rm --name uwscli-devel \
	--hostname devel.uwscli.local \
	-e PYTHONPATH=/srv/home/uwscli/lib \
	-v ${CLI_HOME}/bin:/srv/home/uwscli/bin:ro \
	-v ${CLI_HOME}/etc:/srv/home/uwscli/etc:ro \
	-v ${CLI_HOME}/lib:/srv/home/uwscli/lib:ro \
	-v ${PWD}/cli/test:/srv/home/uwscli/test:ro \
	-u uwscli uws/cli
