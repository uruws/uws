#!/bin/sh
set -eu
cluster=~/cluster/${UWS_CLUSTER}

~/k8s/ca/setup.sh

uwskube apply -f ${cluster}/gateway.yaml
exit 0
