#!/bin/sh
set -eu
uwskube apply -f ~/k8s/nginx-ingress/setup.yaml
exit 0
