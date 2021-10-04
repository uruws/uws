#!/bin/sh
set -eu
#~ uwskube delete -f ~/k8s/dashboard/auth.yaml
uwskube delete -f ~/k8s/dashboard/${K8S_VERSION}/deploy.yaml
exit 0
