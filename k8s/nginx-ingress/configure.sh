#!/bin/sh
set -eu
if test -s ~/cluster/nginx/custom-headers.yaml; then
	uwskube apply -f ~/cluster/nginx/custom-headers.yaml
else
	uwskube apply -f ~/k8s/nginx-ingress/custom-headers.yaml
fi
if test -s ~/cluster/nginx/config.yaml; then
	uwskube apply -f ~/cluster/nginx/config.yaml
else
	uwskube apply -f ~/k8s/nginx-ingress/config.yaml
fi
exit 0
