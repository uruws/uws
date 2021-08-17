#!/bin/sh
set -eu
uwskube delete -f ~/k8s/nginx-ingress/setup-jobs.yaml --wait=true
uwskube apply -f ~/k8s/nginx-ingress/setup.yaml --wait=true
uwskube apply -f ~/k8s/nginx-ingress/setup-jobs.yaml --wait=true
~/k8s/nginx-ingress/deploy.sh
exit 0
