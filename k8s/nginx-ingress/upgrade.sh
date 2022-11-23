#!/bin/sh
set -eu
~/k8s/nginx-ingress/deploy.py --setup-jobs | uwskube delete --wait=true -f -
~/k8s/nginx-ingress/deploy.py --setup      | uwskube apply  --wait=true -f -
~/k8s/nginx-ingress/deploy.py --setup-jobs | uwskube apply  --wait=true -f -
~/k8s/nginx-ingress/deploy.sh
exit 0
