#!/bin/sh
set -eu
uwskube delete -f ~/k8s/nginx-ingress/setup-jobs.yaml
uwskube apply -f ~/k8s/nginx-ingress/setup.yaml
uwskube apply -f ~/k8s/nginx-ingress/setup-jobs.yaml
~/k8s/nginx-ingress/deploy.sh
exit 0
