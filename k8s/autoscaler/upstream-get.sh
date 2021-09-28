#!/bin/sh
set -eu
VERSION='1.19.1'
wget -q -O - https://raw.githubusercontent.com/kubernetes/autoscaler/cluster-autoscaler-${VERSION}/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
exit 0
