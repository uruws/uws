#!/bin/sh
set -eu
uwskube apply -f ~/k8s/dashboard/deploy.yaml
uwskube apply -f ~/k8s/dashboard/auth.yaml
exit 0
