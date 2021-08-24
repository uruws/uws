#!/bin/sh
set -u
uwskube delete svc munin-web
uwskube delete svc k8smon
uwskube delete ingress cluster-gateway --wait=true
uwskube delete secret uwsca-ops
exit 0
