#!/bin/sh
set -eu
uwskube delete -f ~/k8s/nginx-ingress/setup.yaml
exit 0
