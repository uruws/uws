#!/bin/sh
set -eu
env=${1:?'app env?'}
statsdir=${2:-"${HOME}/uws/api/stats"}
authdir=${HOME}/uws/auth
mkdir -vp ${statsdir} ${authdir}
exec docker run --rm \
	--name "uws-heroku-syslog-${env}" \
	--hostname "heroku-syslog-${env}.uws.local" \
	-v "${statsdir}:/home/uws/stats" \
	-v "${authdir}:/home/uws/auth:ro" \
	-u uws \
	-e UWS_LOG=${UWS_LOG:-'quiet'} \
	uws/heroku-logger "${env}"
