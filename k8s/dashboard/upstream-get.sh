#!/bin/sh
set -eu
VERSION='2.0.5'
wget -O - \
	https://raw.githubusercontent.com/kubernetes/dashboard/v${VERSION}/aio/deploy/recommended.yaml
exit 0
