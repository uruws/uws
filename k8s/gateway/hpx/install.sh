#!/bin/sh
set -eu
uwskube delete deploy/defhpx-haproxy-ingress-default-backend -n default || true
exec ~/k8s/haproxy/install.sh k8s/gateway/hpx
