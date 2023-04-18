#!/bin/sh
set -eu
exec uwskube rollout restart deployment.apps/kube-state-metrics -n grfn
