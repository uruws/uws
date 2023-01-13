#!/bin/sh
set -eu
helm upgrade --install netdata netdata \
	--repo https://netdata.github.io/helmchart/ \
	--namespace netdata \
	--create-namespace \
	--values ./k8s/netdata/values.yaml
exit 0
