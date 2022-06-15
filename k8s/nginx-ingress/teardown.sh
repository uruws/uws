#!/bin/sh
set -eu
if test -s ~/cluster/nginx/config.yaml; then
	uwskube delete -f ~/cluster/nginx/config.yaml
else
	uwskube delete -f ~/k8s/nginx-ingress/config.yaml
fi
uwskube delete -f ~/k8s/nginx-ingress/${K8S_VERSION}/deploy.yaml
uwskube delete -f ~/k8s/nginx-ingress/${K8S_VERSION}/setup-jobs.yaml
uwskube delete -f ~/k8s/nginx-ingress/${K8S_VERSION}/setup.yaml
exit 0
