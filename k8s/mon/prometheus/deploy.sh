#!/bin/sh
set -eu
exec uwskube apply --kustomize github.com/kubernetes/ingress-nginx/deploy/prometheus/
