#!/bin/sh
set -eu

INGRESS_NAME=${1:?'ingress?'}
export INGRESS_NAME

envsubst <~/k8s/offline-page/patch.yaml >/tmp/offline-page.patch-${INGRESS_NAME}
uwskube patch ingress "${INGRESS_NAME}" --patch-file=/tmp/offline-page.patch-${INGRESS_NAME}

rm -f /tmp/offline-page.patch-${INGRESS_NAME}
exit 0
