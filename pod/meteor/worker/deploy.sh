#!/bin/sh
set -eu
appver=${1:-''}
pod=/home/uws/pod/meteor/worker
if test "X${appver}" != 'X'; then
	~/pod/meteor/setcfg.sh "${appver}"
fi
envf=$(mktemp -p /tmp meteor-worker-deploy.XXXXXXXX)
~/pod/meteor/getcfg.sh >${envf}
cat ${envf}
. ${envf}
rm -f ${envf}
envsubst <${pod}/deploy.yaml | uwskube apply -f -
exit 0
