#!/bin/sh
set -eu
env=${1:?'app env?'}
. /home/uws/auth/heroku.env
export UWS_LOG=${UWS_LOG:-'quiet'}
stdir=/home/uws/stats
mkdir -p ${stdir}/${env}
app="tapo${env}"
if test 'Xproduction' = "X${env}"; then
	app="tapo"
fi
exec heroku logs -a "${app}" -s app -d web | grep -F ': PARSER' | sort -k1,1 -u |
	api-logs -env ${env} -statedir ${stdir} -statsdir ${stdir} -kind heroku -filter -
