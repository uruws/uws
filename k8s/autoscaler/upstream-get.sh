#!/bin/sh
set -eu
# https://github.com/kubernetes/autoscaler/tags
VERSION='1.25.0'
wget -q -O - https://raw.githubusercontent.com/kubernetes/autoscaler/cluster-autoscaler-${VERSION}/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
exit 0
