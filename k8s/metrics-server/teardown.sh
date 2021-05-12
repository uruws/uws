#!/bin/sh
set -eu
uwskube delete -f ~/k8s/metrics-server/setup.yaml
exit 0
