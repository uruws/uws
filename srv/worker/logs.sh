#!/bin/sh
set -eu
appenv=${1:?'app env?'}
shift

myfn=$(realpath -e $0)
mydir=$(dirname ${myfn})
compose=${mydir}/compose.yaml
srv_compose=${mydir}/compose-server.yaml

exec docker-compose -f "${compose}" -f "${srv_compose}" -p "${appenv}" \
	logs $@ meteor-worker
