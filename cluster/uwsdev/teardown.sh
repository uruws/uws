#!/bin/sh
set -eu
cluster=~/cluster/${UWS_CLUSTER}
uwskube delete -f ${cluster}/gateway.yaml

~/k8s/ca/teardown.sh
exit 0
