#!/bin/sh
set -eu
# smtps CA
CA=${HOME}/ca/uws/smtps/211006/client
uwskube delete secret smtps-ca -n mon || true
uwskube create secret generic smtps-ca -n mon \
	--from-file="${CA}"

# cluster.conf
conf=/tmp/mon.munin.cluster.conf
envsubst <~/k8s/mon/munin/conf.d/cluster.conf >${conf}
uwskube delete configmap munin-confd -n mon || true
uwskube create configmap munin-confd -n mon \
	--from-file="cluster.conf=${conf}"
exit 0
