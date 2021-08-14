#!/bin/sh
set -eu

cluster_setup=${HOME}/k8s/mon/munin-node/utils/cluster-setup.sh
uwskube delete configmap cluster-setup -n mon || true
uwskube create configmap cluster-setup -n mon \
	--from-file="setup.sh=${cluster_setup}"

export VERSION="$(cat ~/k8s/mon/VERSION)"
envsubst <~/k8s/mon/munin-node/deploy.yaml | uwskube apply -f -

exit 0
