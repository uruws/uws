#!/bin/sh
set -eu
ns=${1:?'app namespace?'}
app=${2:?'app name?'}
appver=${3:-''}
pod=${HOME}/pod/meteor/${app}
if test "X${appver}" != 'X'; then
	~/pod/meteor/setcfg.sh "${ns}" "${app}" "${appver}"
fi
envf=$(mktemp -p /tmp meteor-${app}-deploy.XXXXXXXX)
~/pod/meteor/getcfg.sh "${app}" >${envf}
cat ${envf}

# shellcheck disable=SC1090
. ${envf}

rm -f ${envf}
envsubst <${pod}/deploy.yaml | uwskube apply -f -
exit 0
