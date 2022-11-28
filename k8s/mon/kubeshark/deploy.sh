#!/bin/sh
set -eu

nss=${1:?'namespaces?'}

envsubst '${CLUSTER_HOST}' <~/k8s/kubeshark/gateway.yaml | uwskube apply -f -

#~/k8s/mon/k8s/configure.sh

VERSION="$(cat ~/k8s/mon/VERSION)"
export VERSION

KUBESHARK_NAMESPACES="${nss}"
export KUBESHARK_NAMESPACES

envsubst <~/k8s/mon/kubeshark/deploy.yaml | uwskube apply -f -

exit 0
