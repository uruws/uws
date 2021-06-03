#!/bin/sh
set -eu

uwskube create namespace mon

# github.com/timescale/timescaledb-kubernetes/blob/master/
#	charts/timescaledb-single/admin-guide.md#credentials

uwskube create secret generic tobs-credentials -n mon \
	--from-env-file=${HOME}/secret/tobs/credentials

uwskube apply -n mon -f ~/k8s/ca/deploy.yaml
uwskube apply -n mon -f ~/k8s/tobs/certificate.yaml

helm repo add timescale https://charts.timescale.com/
helm repo update
helm upgrade --install --version 0.4.1 -f ~/k8s/tobs/values.yaml \
	--namespace mon --devel tobs timescale/tobs

exit 0
