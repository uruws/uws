#!/bin/sh
set -eu
uwskube apply -f ~/k8s/nginx-ingress/deploy.yaml
exit 0
