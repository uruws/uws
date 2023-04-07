#!/bin/sh
set -eu
exec uwskube logs -n grfn --prefix -c config-reloader \
	-l operator.agent.grafana.com/type=integrations "$@"
