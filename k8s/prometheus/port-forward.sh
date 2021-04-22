#!/bin/sh
set -eu
. ~/bin/env.export

POD_NAME=$(uwskube get pods --namespace prometheus -l "app=prometheus,component=server" -o jsonpath="{.items[0].metadata.name}")
uwskube --namespace prometheus port-forward --address 0.0.0.0 ${POD_NAME} 9090 &
echo "--- Prometheus: ${POD_NAME}:9090 localhost:9090"

POD_NAME=$(uwskube get pods --namespace prometheus -l "app=prometheus,component=alertmanager" -o jsonpath="{.items[0].metadata.name}")
uwskube --namespace prometheus port-forward --address 0.0.0.0 ${POD_NAME} 9093 &
echo "--- Prometheus Alertmanager: ${POD_NAME}:9093 localhost:9093"

POD_NAME=$(uwskube get pods --namespace prometheus -l "app=prometheus,component=pushgateway" -o jsonpath="{.items[0].metadata.name}")
uwskube --namespace prometheus port-forward --address 0.0.0.0 ${POD_NAME} 9091 &
echo "--- Prometheus PushGateway: ${POD_NAME}:9091 localhost:9091"

exit 0
