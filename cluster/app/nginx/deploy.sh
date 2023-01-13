#!/bin/sh
set -eu
~/k8s/nginx-ingress/deploy.py --deploy --cpu 100 --mem 512 |
	uwskube apply -f -
exit 0
