#!/bin/sh
set -eu
if test -s ~/cluster/nginx/config.yaml; then
	uwskube delete -f ~/cluster/nginx/config.yaml
else
	uwskube delete -f ~/k8s/nginx-ingress/config.yaml
fi
uwskube delete -f ~/k8s/nginx-ingress/deploy.yaml
uwskube delete -f ~/k8s/nginx-ingress/setup-jobs.yaml
uwskube delete -f ~/k8s/nginx-ingress/setup.yaml
exit 0
