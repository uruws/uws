#!/bin/sh
set -eu
exec uwskube rollout restart daemonset.apps/grafana-agent-integrations-ds -n grfn
