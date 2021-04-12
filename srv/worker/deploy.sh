#!/bin/sh
set -eu
appname=${1:?'app name?'}
appenv=${2:?'app env?'}
export APP=${appname}

myfn=$(realpath -e $0)
mydir=$(dirname ${myfn})
compose=${mydir}/compose.yaml
srv_compose=${mydir}/compose-server.yaml

app_scale=${APP_SCALE:-'10'}

#~ docker stack deploy -c "${compose}" -c "${srv_compose}" "${appenv}"

exec docker-compose -f "${compose}" -f "${srv_compose}" -p "${appenv}" \
	up --no-build --no-color --timeout 15 \
	--scale meteor-worker=${app_scale} meteor-worker
