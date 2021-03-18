#!/bin/sh
set -eu

BUILD_CACHE=${PWD}/build/go-cache
mkdir -vp ${BUILD_CACHE}

SRCDIR=${UWS_SRCDIR:-'/opt/src/TalkingPts'}
mkdir -vp ${SRCDIR}/MonitoringBots

mkdir -vp ${HOME}/.uws/golang ${PWD}/build/uwsbot/stats

exec docker run -it --rm --name uwsbot-devel \
	--hostname uwsbot-devel.uws.local \
	-v ${PWD}/go:/go/src/uws \
	-v ${SRCDIR}:/uws/src \
	-v ${BUILD_CACHE}:/go/.cache \
	-v ${HOME}/.uws/golang/bot:/home/uws/.config/uws/bot:ro \
	-v ${PWD}/build/uwsbot/stats:/uws/var/uwsbot/stats \
	--entrypoint /usr/local/bin/uws-login.sh \
	-u uws uws/golang
