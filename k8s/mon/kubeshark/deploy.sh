#!/bin/sh
set -eu

nss=${1:?'namespaces?'}

#~/k8s/mon/k8s/configure.sh

VERSION="$(cat ~/k8s/mon/VERSION)"
export VERSION

KUBESHARK_NAMESPACES="${nss}"
export KUBESHARK_NAMESPACES

envsubst <~/k8s/mon/kubeshark/deploy.yaml | uwskube apply -f -

exec ~/k8s/mon/kubeshark/gw/deploy.sh
