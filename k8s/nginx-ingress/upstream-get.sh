#!/bin/sh
set -eu
VERSION='0.48.1'
wget -O upstream-deploy.yaml https://github.com/kubernetes/ingress-nginx/raw/controller-v${VERSION}/deploy/static/provider/aws/deploy.yaml
exit 0
