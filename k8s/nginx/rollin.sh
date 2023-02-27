#!/bin/sh
set -u

ns=${1:?'namespace?'}
gw=${2:?'gateway?'}

uwskube delete deploy proxy         -n "${ns}"
uwskube delete secret sites-enabled -n "${ns}"

svcd=${gw}/service
if test -d "${svcd}"; then
	uwskube delete -n "${ns}" -f "${svcd}"
fi

~/ca/godaddyCerts/teardown.sh "${ns}"
~/ca/uws/ops/teardown.sh "${ns}"
~/ca/uwsgd/teardown.sh "${ns}"

exit 0
