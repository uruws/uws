#!/bin/sh
set -eu
uwskube delete configmap provision-datasources -n mon
uwskube delete configmap provision-dashboards -n mon
uwskube delete configmap dashboard-uws -n mon
uwskube delete configmap grafcfg -n mon
uwskube delete configmap promcfg -n mon
uwskube delete namespace mon
exit 0
