#!/bin/sh
set -eu
exec uwskube rollout restart daemonset.apps/grafana-agent-logs -n grfn
