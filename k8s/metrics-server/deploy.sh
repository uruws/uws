#!/bin/sh
set -eu
uwskube apply -f ~/k8s/metrics-server/deploy.yaml
exit 0
