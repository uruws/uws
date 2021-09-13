#!/bin/sh
set -eu
if test -s ~/cluster/nginx/config.yaml; then
	uwskube apply -f ~/cluster/nginx/config.yaml
else
	uwskube apply -f ~/k8s/nginx-ingress/config.yaml
fi
uwskube apply -f ~/k8s/nginx-ingress/deploy.yaml
exit 0
