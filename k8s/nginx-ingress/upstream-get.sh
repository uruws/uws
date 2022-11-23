#!/bin/sh
set -eu
VERSION='1.5.1'
K8S_VERSION='1.22'
BASE=https://github.com/kubernetes/ingress-nginx/raw
FPATH=deploy/static/provider/aws/deploy.yaml
DST=./k8s/nginx-ingress/${K8S_VERSION}/upstream.yaml
exec wget -O "${DST}" "${BASE}/controller-v${VERSION}/${FPATH}"
