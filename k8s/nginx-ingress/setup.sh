#!/bin/sh
set -eu
~/k8s/nginx-ingress/deploy.py --setup      | uwskube apply -f -
~/k8s/nginx-ingress/deploy.py --setup-jobs | uwskube apply -f -
exec ~/k8s/nginx-ingress/deploy.sh
