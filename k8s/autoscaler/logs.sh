#!/bin/sh
set -eu
. ~/bin/env.export
exec uwskube -n kube-system logs deployment.apps/cluster-autoscaler $@
