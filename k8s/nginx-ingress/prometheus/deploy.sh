#!/bin/sh
set -eu
uwskube apply --kustomize github.com/kubernetes/ingress-nginx/deploy/prometheus/
uwskube patch service prometheus-server -n ingress-nginx \
	--patch-file=${HOME}/k8s/nginx-ingress/prometheus/patch.yaml
exit 0
