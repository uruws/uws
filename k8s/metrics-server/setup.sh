#!/bin/sh
set -eu
. ~/bin/env.export
uwskube apply -f ~/k8s/metrics-server/deploy.yaml
exit 0
