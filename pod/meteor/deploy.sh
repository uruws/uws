#!/bin/sh
set -eu
ns=${1:?'app namespace?'}
app=${2:?'app name?'}
appver=${3:-''}
pod=${HOME}/pod/meteor/${app}
if test "X${appver}" != 'X'; then
	~/pod/meteor/setcfg.sh "${ns}" "${appver}"
fi
envf=$(mktemp -p /tmp meteor-${ns}-deploy.XXXXXXXX)
~/pod/meteor/getcfg.sh "${ns}" >${envf}
cat ${envf}

# shellcheck disable=SC1090
. ${envf}
rm -f ${envf}

envsubst <${pod}/deploy.yaml | uwskube apply -f -

~/pod/lib/rollback-setcfg.sh "${ns}" "${appver}"
exit 0
