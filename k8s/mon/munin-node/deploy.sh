#!/bin/sh
set -eu

cluster_setup=${HOME}/k8s/mon/munin-node/utils/cluster-setup.sh
node_conf=${HOME}/k8s/mon/munin-node/node.conf

uwskube delete configmap cluster-setup -n mon || true
uwskube create configmap cluster-setup -n mon \
	--from-file="setup.sh=${cluster_setup}" \
	--from-file="munin-node.conf=${node_conf}"

export VERSION="$(cat ~/k8s/mon/VERSION)"
envsubst <~/k8s/mon/munin-node/deploy.yaml | uwskube apply -f -

exit 0
