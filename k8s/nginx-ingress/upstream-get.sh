#!/bin/sh
set -eu
VERSION='1.2.1'
wget -O - \
	https://github.com/kubernetes/ingress-nginx/raw/controller-v${VERSION}/deploy/static/provider/aws/deploy.yaml |
	grep -vF '#GENERATED FOR K8S' >upstream-deploy.yaml
exit 0
