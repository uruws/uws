#!/bin/sh
set -eu
~/k8s/nginx-ingress/configure.sh
exec uwskube rollout -n ingress-nginx restart deployment
