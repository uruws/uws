#!/bin/sh
set -eu
if test -s ~/cluster/nginx/config.yaml; then
	uwskube delete -f ~/cluster/nginx/config.yaml
else
	uwskube delete -f ~/k8s/nginx-ingress/config.yaml
fi
exec ~/k8s/nginx-ingress/helm/uninstall.sh
