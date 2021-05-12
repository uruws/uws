#!/bin/sh
set -eu
uwskube apply -f ~/k8s/metrics-server/setup.yaml
exit 0
