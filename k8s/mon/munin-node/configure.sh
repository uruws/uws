#!/bin/sh
set -eu

# setup

cluster_setup=${HOME}/k8s/mon/munin-node/utils/cluster-setup.sh
node_conf=${HOME}/k8s/mon/munin-node/node.conf

uwskube delete configmap node-setup -n mon || true
uwskube create configmap node-setup -n mon \
	--from-file="setup.sh=${cluster_setup}" \
	--from-file="munin-node.conf=${node_conf}"

# plugins

plugins=${HOME}/k8s/mon/munin-node/plugins

uwskube delete configmap munin-plugins -n mon || true
uwskube create configmap munin-plugins -n mon \
	--from-file="${plugins}/"

# ops ca

opsca=${HOME}/ca/uws/ops/etc
opsca_client=${HOME}/ca/uws/ops/210823/client
opsca_cert='12a549fb-96a3-5131-aa15-9bc30cc7d99d'

grep -F "${opsca_cert}" ${opsca}/client.pw >/tmp/opsca_client

uwskube delete configmap ops-ca -n mon || true
uwskube create configmap ops-ca -n mon \
	--from-file="client.pw=/tmp/opsca_client"

rm -f /tmp/opsca_client

uwskube delete configmap ops-ca-client -n mon || true
uwskube create configmap ops-ca-client -n mon \
	--from-file="${opsca_cert}.pem=${opsca_client}/${opsca_cert}.pem" \
	--from-file="${opsca_cert}-key.pem=${opsca_client}/${opsca_cert}-key.pem"

exit 0
