#!/bin/sh
set -eu
uwskube delete configmap promcfg -n mon || true
uwskube create configmap promcfg -n mon --from-file=${HOME}/mon/etc/prometheus/

uwskube delete configmap grafcfg -n mon || true
uwskube create configmap grafcfg -n mon --from-file=${HOME}/mon/etc/grafana/

uwskube delete configmap dashboard-uws -n mon || true
uwskube create configmap dashboard-uws -n mon --from-file=${HOME}/mon/dashboard/uws/

uwskube delete configmap provision-dashboards -n mon || true
uwskube create configmap provision-dashboards -n mon \
	--from-file=${HOME}/mon/etc/grafana/provisioning/dashboards/

uwskube delete configmap provision-datasources -n mon || true
uwskube create configmap provision-datasources -n mon \
	--from-file=${HOME}/mon/etc/grafana/provisioning/datasources/
exit 0
