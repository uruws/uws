#!/bin/sh
set -eu
exec uwskube delete --kustomize github.com/kubernetes/ingress-nginx/deploy/prometheus/
