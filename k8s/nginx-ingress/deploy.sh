#!/bin/sh
set -eu
. ~/bin/env.export
uwskube apply -f ~/k8s/nginx-ingress/deploy.yaml
exit 0
