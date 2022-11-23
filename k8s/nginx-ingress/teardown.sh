#!/bin/sh
set -eu
if test -s ~/cluster/nginx/config.yaml; then
	uwskube delete -f ~/cluster/nginx/config.yaml
else
	uwskube delete -f ~/k8s/nginx-ingress/config.yaml
fi
~/k8s/nginx-ingress/deploy.py --deploy     | uwskube delete -f -
~/k8s/nginx-ingress/deploy.py --setup-jobs | uwskube delete -f -
~/k8s/nginx-ingress/deploy.py --setup      | uwskube delete -f -
exit 0
