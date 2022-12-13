#!/bin/sh
set -u
helm uninstall --namespace ingress-nginx ingress-nginx
uwskube delete namespace ingress-nginx
exit 0
