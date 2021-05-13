#!/bin/sh
set -eu
. ~/bin/env.export
uwskube apply -f ~/k8s/ca/deploy.yaml
exit 0
