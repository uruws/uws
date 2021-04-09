#!/bin/sh
set -eu
appname=${1:?'app name?'}
appenv=${2:?'app env?'}
export APP=${appname}
myfn=$(realpath -e $0)
mydir=$(dirname ${myfn})
compose=${mydir}/compose.yaml
srv_compose=${mydir}/compose-server.yaml
docker stack deploy -c "${compose}" -c "{srv_compose}" "${appenv}"
exit 0
