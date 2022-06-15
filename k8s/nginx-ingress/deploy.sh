#!/bin/sh
set -eu
~/k8s/nginx-ingress/configure.sh
exec uwskube apply -f ~/k8s/nginx-ingress/${K8S_VERSION}/deploy.yaml
