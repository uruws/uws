#!/bin/sh
set -eu
uwskube delete -f ~/k8s/dashboard/auth.yaml
uwskube delete -f ~/k8s/dashboard/deploy.yaml
exit 0
