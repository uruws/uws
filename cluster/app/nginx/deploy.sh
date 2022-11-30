#!/bin/sh
set -eu
~/k8s/nginx-ingress/deploy.py --deploy --replicas 3
	| uwskube apply -f -
exit 0
