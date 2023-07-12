#!/bin/sh
set -eu
helm upgrade --install grafana grafana-agent-operator \
	--repo https://grafana.github.io/helm-charts \
	--namespace grfn
exec ~/k8s/grafana/deploy.sh
