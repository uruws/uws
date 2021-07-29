#!/bin/sh
set -eu

cluster=${UWS_CLUSTER}

sed "s#\[UWS_CLUSTER]#${cluster}#" ~/k8s/autoscaler/deploy.yaml.in >/tmp/cluster-autoscaler-${cluster}.yaml

uwskube delete -f /tmp/cluster-autoscaler-${cluster}.yaml

exit 0
