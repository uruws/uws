#!/bin/sh
set -eu

ns=${1:?'namespace?'}
app=${2:?'app name?'}
appver=${3:?'app version?'}

~/pod/lib/tapo3/configure.sh "${ns}" "${app}" "${appver}"

METEOR_CLUSTER="${UWS_CLUSTER}"
export METEOR_CLUSTER

METEOR_ENV="${TAPO3_ENV}"
export METEOR_ENV

METEOR_APP="${app}"
export METEOR_APP

METEOR_NAMESPACE="${ns}"
export METEOR_NAMESPACE

METEOR_VERSION="${appver}"
export METEOR_VERSION

~/pod/lib/tapo3/ngx/configure.sh "${ns}" "${app}"

METEOR_DEPLOY=$(date '+%y%m%d.%H%M%S')
export METEOR_DEPLOY

if test 'Xtrue' = "X${METEOR_HPA_ENABLE:-false}"; then
	envsubst <~/pod/lib/tapo3/deploy.yaml | grep -vF '  replicas: ' | uwskube apply -f -
	envsubst <~/pod/lib/tapo3/deploy-hpa.yaml | uwskube apply -f -
else
	uwskube delete hpa "meteor-${app}-hpa" -n "${ns}" || true
	envsubst <~/pod/lib/tapo3/deploy.yaml | uwskube apply -f -
fi

~/pod/lib/tapo3/ngx/ingress-deploy.sh "${ns}" "${app}"

~/pod/lib/tapo3/deploy-setver.sh "${ns}" "${app}" "${appver}"

exit 0
