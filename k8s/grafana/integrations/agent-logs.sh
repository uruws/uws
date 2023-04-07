#!/bin/sh
set -eu
exec uwskube logs -n grfn --prefix -c grafana-agent \
	-l operator.agent.grafana.com/type=integrations "$@"
