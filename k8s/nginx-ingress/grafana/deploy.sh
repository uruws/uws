#!/bin/sh
set -eu
uwskube apply --kustomize github.com/kubernetes/ingress-nginx/deploy/grafana/
uwskube patch service grafana -n ingress-nginx \
	--patch-file=${HOME}/k8s/nginx-ingress/grafana/patch.yaml
exit 0
