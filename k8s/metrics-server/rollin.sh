#!/bin/sh
set -eu
uwskube delete -f ~/k8s/metrics-server/deploy.yaml
exit 0
