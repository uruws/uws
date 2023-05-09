#!/bin/sh
set -eu

# smtps CA
uwskube delete secret smtps-ca -n mon || true

# smtps CA client
uwskube delete secret smtps-ca-client -n mon || true

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
uwskube delete secret munin-crond -n mon || true
uwskube create secret generic munin-crond -n mon --from-file="${crond}"

# munin-deploy-conf
deploy_confd=${HOME}/secret/munin/conf
uwskube delete secret munin-deploy-confd -n mon || true
uwskube create secret generic munin-deploy-confd -n mon \
	--from-file="${deploy_confd}"

exit 0
