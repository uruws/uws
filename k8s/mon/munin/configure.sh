#!/bin/sh
set -eu
conf=/tmp/mon.munin.cluster.conf
envsubst <~/k8s/mon/munin/conf.d/cluster.conf >${conf}
uwskube delete configmap munin-confd -n mon || true
uwskube create configmap munin-confd -n mon \
	--from-file="cluster.conf=${conf}"
exit 0
