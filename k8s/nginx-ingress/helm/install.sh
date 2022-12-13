#!/bin/sh
set -eu
helm upgrade --install ingress-nginx ingress-nginx \
	--repo https://kubernetes.github.io/ingress-nginx \
	--namespace ingress-nginx \
	--create-namespace \
	--values ./k8s/nginx-ingress/helm/values.yaml
exit 0
