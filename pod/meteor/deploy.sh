#!/bin/sh
set -eu
ns=${1:?'app namespace?'}
app=${2:?'app name?'}
appver=${3:-''}
pod=${HOME}/pod/meteor/${app}

export UWSPOD_GETCFG='meteor/getcfg'
~/pod/lib/rollback-setcfg.sh "${ns}" "${appver}"

if test "X${appver}" != 'X'; then
	~/pod/meteor/setcfg.sh "${ns}" "${appver}"
fi
envf=$(mktemp -p /tmp meteor-${ns}-deploy.XXXXXXXX)
~/pod/meteor/getcfg.sh "${ns}" >${envf}
cat ${envf}

# shellcheck disable=SC1090
. ${envf}
rm -f ${envf}

export APP_CLUSTER="${UWS_CLUSTER}"
export APP_ENV="${APP_ENV}"
export APP_NAMESPACE="${ns}"
export APP_VERSION="${appver}"

APP_DEPLOY=$(date '+%y%m%d.%H%M%S')
export APP_DEPLOY

envsubst <${pod}/deploy.yaml | uwskube apply -f -
exit 0
