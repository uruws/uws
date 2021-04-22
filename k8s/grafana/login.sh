#!/bin/sh
set -eu
. ~/bin/env.export

uwskube get secret --namespace prometheus loki-grafana \
	-o jsonpath="{.data.admin-password}" | base64 --decode; echo

POD_NAME=$(uwskube get pods --namespace prometheus -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=loki-grafana" -o jsonpath="{.items[0].metadata.name}")

echo "uwskube --namespace prometheus port-forward ${POD_NAME} 3000"

exit 0
