#!/bin/sh
set -eu

cluster_setup=${HOME}/k8s/mon/munin-node/utils/cluster-setup.sh
node_conf=${HOME}/k8s/mon/munin-node/node.conf

uwskube delete configmap node-setup -n mon || true
uwskube create configmap node-setup -n mon \
	--from-file="setup.sh=${cluster_setup}" \
	--from-file="munin-node.conf=${node_conf}"

plugins=${HOME}/k8s/mon/munin-node/plugins

uwskube delete configmap munin-plugins -n mon || true
uwskube create configmap munin-plugins -n mon \
	--from-file="${plugins}/"

exit 0
