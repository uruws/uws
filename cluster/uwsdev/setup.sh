#!/bin/sh
set -eu
cluster=~/cluster/${UWS_CLUSTER}
uwskube apply -f ${cluster}/gateway.yaml
exit 0
