#!/bin/sh
set -eu
helm uninstall --namespace ingress-nginx ingress-nginx
exec uwskube delete namespace ingress-nginx
