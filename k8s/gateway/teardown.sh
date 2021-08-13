#!/bin/sh
set -eu
uwskube delete svc munin-web
uwskube delete svc k8smon
uwskube delete ingress cluster-gateway
exit 0
