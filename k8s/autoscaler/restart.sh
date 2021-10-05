#!/bin/sh
set -eu
exec uwskube rollout -n kube-system restart deployment/cluster-autoscaler
