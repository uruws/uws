#!/bin/sh
set -eu
appver=${1:-''}
pod=/home/uws/pod/meteor/web
if test "X${appver}" != 'X'; then
	~/pod/meteor/setcfg.sh "${appver}"
fi
envf=$(mktemp -p /tmp meteor-web-deploy.XXXXXXXX)
~/pod/meteor/getcfg.sh >${envf}
cat ${envf}
. ${envf}
rm -f ${envf}
envsubst <${pod}/deploy.yaml | uwskube apply -f -
exit 0
