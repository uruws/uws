#!/bin/sh
set -eu
. ~/bin/env.export
uwskube apply -f ~/k8s/dashboard/deploy.yaml
uwskube apply -f ~/k8s/dashboard/auth.yaml
exit 0
