#!/bin/sh
set -eu

appver=${1:?'app version?'}

set -x

export TAPO_ENV="${SRMNT_ENV}"
export TAPO_NAMESPACE="${SRMNT_NAMESPACE}"
export TAPO_REPLICAS="${SRMNT_WEB_REPLICAS}"
export TAPO_CDN_REPLICAS="${SRMNT_CDN_REPLICAS}"
export TAPO_API_REPLICAS="${SRMNT_API_REPLICAS}"

~/pod/tapo/api/deploy.sh "${appver}"
~/pod/tapo/web/deploy.sh "${appver}"

~/pod/tapo/api/wait.sh
~/pod/tapo/web/wait.sh

exit 0
