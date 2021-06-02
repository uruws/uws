#!/bin/sh
set -eu
helm uninstall --namespace mon tobs || true

uwskube delete secret tobs-credentials -n mon

uwskube delete -n mon -f ~/k8s/tobs/certificate.yaml
uwskube delete -n mon -f ~/k8s/ca/deploy.yaml

uwskube delete namespace mon
exit 0
