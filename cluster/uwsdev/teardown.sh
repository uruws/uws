#!/bin/sh
set -eu
cluster=~/cluster/${UWS_CLUSTER}
uwskube delete -f ${cluster}/gateway.yaml
exit 0
