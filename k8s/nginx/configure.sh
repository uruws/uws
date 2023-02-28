#!/bin/sh
set -eu

ns=${1:?'namespace?'}
gw=${2:?'gateway?'}

# sites-enabled
uwskube delete secret sites-enabled -n "${ns}" || true
uwskube create secret generic sites-enabled -n "${ns}" \
	--from-file="${gw}/nginx/sites-enabled"

svcd=${gw}/nginx/service
if test -d "${svcd}"; then
	uwskube apply -n "${ns}" -f "${svcd}"
fi

~/ca/godaddyCerts/setup.sh "${ns}"
~/ca/uws/ops/setup.sh "${ns}"
~/ca/uwsgd/setup.sh "${ns}"

exit 0
