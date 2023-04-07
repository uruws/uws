#!/bin/sh
set -eu
exec uwskube rollout restart deployment.apps/grafana-agent-integrations-deploy -n grfn
