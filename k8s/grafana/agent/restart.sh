#!/bin/sh
set -eu
exec uwskube rollout restart statefulset.apps/grafana-agent -n grfn
