#!/bin/sh
set -eu
VERSION='1.5.1'
BASE=https://github.com/kubernetes/ingress-nginx/raw
FPATH=deploy/static/provider/aws/deploy.yaml
exec wget -O ./k8s/nginx-ingress/upstream-deploy.yaml \
	"${BASE}/controller-v${VERSION}/${FPATH}"
