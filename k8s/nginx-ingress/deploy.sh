#!/bin/sh
set -eu
~/k8s/nginx-ingress/configure.sh
~/k8s/nginx-ingress/deploy.py --deploy | uwskube apply -f -
exit 0
