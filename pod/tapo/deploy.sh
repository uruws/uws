#!/bin/sh
set -eu

ns=${1:?'namespace?'}
app=${2:?'app name?'}
appver=${3:?'app version?'}

~/pod/tapo/configure.sh "${ns}" "${app}" "${appver}"

METEOR_CLUSTER="${UWS_CLUSTER}"
export METEOR_CLUSTER

METEOR_ENV="${TAPO_ENV}"
export METEOR_ENV

METEOR_APP="${app}"
export METEOR_APP

METEOR_NAMESPACE="${ns}"
export METEOR_NAMESPACE

METEOR_VERSION="${appver}"
export METEOR_VERSION

METEOR_DEPLOY=$(date '+%y%m%d.%H%M%S')
export METEOR_DEPLOY

envsubst <~/pod/tapo/deploy.yaml | uwskube apply -f -

~/pod/tapo/deploy-setver.sh "${ns}" "${app}" "${appver}"

exit 0
