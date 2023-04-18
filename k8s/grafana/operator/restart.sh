#!/bin/sh
set -eu
exec uwskube rollout restart deployment.apps/grafana-grafana-agent-operator -n grfn
