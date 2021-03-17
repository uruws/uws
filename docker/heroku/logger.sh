#!/bin/sh
set -eu
env=${1:?'app env?'}
authdir=${HOME}/uws/auth
mkdir -vp ${authdir}
exec docker run -it --rm \
	--name "uws-heroku-syslog-${env}" \
	--hostname "heroku-syslog-${env}.uws.local" \
	-v "${authdir}:/home/uws/auth:ro" \
	--log-driver syslog \
	-u uws \
	uws/heroku /usr/local/bin/logger.sh "${env}"
