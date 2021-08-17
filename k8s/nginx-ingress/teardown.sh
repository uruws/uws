#!/bin/sh
set -eu
uwskube delete -f ~/k8s/nginx-ingress/deploy.yaml
uwskube delete -f ~/k8s/nginx-ingress/setup-jobs.yaml
uwskube delete -f ~/k8s/nginx-ingress/setup.yaml
exit 0
