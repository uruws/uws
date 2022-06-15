#!/bin/sh
set -eu
uwskube apply -f ~/k8s/nginx-ingress/${K8S_VERSION}/setup.yaml
uwskube apply -f ~/k8s/nginx-ingress/${K8S_VERSION}/setup-jobs.yaml
exec ~/k8s/nginx-ingress/deploy.sh
