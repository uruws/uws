#!/bin/sh
set -eu
. ~/bin/env.export
exec uwskube -n kube-system logs -f deployment.apps/cluster-autoscaler
