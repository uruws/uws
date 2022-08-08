#!/bin/sh
set -eu

APP_NAMESPACE=${1:?'namespace?'}
export APP_NAMESPACE

INGRESS_NAME=${2:?'ingress?'}
export INGRESS_NAME

envsubst <~/k8s/offline-page/setup.yaml | uwskube apply -f -

envsubst <~/k8s/offline-page/patch.yaml >/tmp/offline-page.patch-${APP_NAMESPACE}
uwskube patch ingress "${INGRESS_NAME}" --patch-file=/tmp/offline-page.patch-${APP_NAMESPACE}

rm -f /tmp/offline-page.patch-${APP_NAMESPACE}
exit 0
