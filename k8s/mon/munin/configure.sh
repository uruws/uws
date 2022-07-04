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

# cluster_local.conf
local_conf=${HOME}/cluster/munin/conf.d/cluster_local.conf
if test -s ${local_conf}; then
	echo '# cluster_local.conf' >>${conf}
	envsubst <${local_conf} >>${conf}
fi

# munin-confd
uwskube delete configmap munin-confd -n mon || true
uwskube create configmap munin-confd -n mon \
	--from-file="cluster.conf=${conf}"

# munin-crond
crond=${HOME}/secret/munin/cron.d
uwskube delete configmap munin-crond -n mon || true
uwskube create configmap munin-crond -n mon --from-file="${crond}"

exit 0
