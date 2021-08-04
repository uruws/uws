#!/bin/sh
set -eu
app=${1:?'app name?'}
appver=${2:-''}
pod=${HOME}/pod/meteor/${app}
if test "X${appver}" != 'X'; then
	~/pod/meteor/setcfg.sh "${app}" "${appver}"
fi
envf=$(mktemp -p /tmp meteor-${app}-deploy.XXXXXXXX)
~/pod/meteor/getcfg.sh "${app}" >${envf}
cat ${envf}
. ${envf}
rm -f ${envf}
envsubst <${pod}/deploy.yaml | uwskube apply -f -
exit 0
