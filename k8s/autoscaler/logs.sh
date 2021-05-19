#!/bin/sh
set -eu
exec uwskube logs deploy/cluster-autoscaler -n kube-system --tail=1 $@
