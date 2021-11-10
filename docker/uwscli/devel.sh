#!/bin/sh
set -eu

CLI_HOME=${PWD}/host/assets/jsbatch/srv/home/uwscli
SRC_DIR=/opt/src/TalkingPts

exec docker run -it --rm --name uwscli-devel \
	--hostname uwscli-devel.uws.local \
	-v ${CLI_HOME}/bin:/srv/home/uwscli/bin:ro \
	-v ${CLI_HOME}/etc:/srv/home/uwscli/etc:ro \
	-v ${SRC_DIR}:/srv/deploy:ro \
	-v ${PWD}:/srv/uws/deploy:ro \
	-u uwscli uws/cli
