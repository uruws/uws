#!/bin/sh
set -eu
appname=${1:?'app name?'}
appenv=${2:?'app env?'}
export APP=${appname}
docker stack deploy -c /srv/uws/deploy/srv/api/compose.yaml "${appenv}"
exit 0
