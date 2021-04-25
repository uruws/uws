#!/bin/sh
set -eu
#exec uwskube logs --tail=10 -n ingress-nginx service/ingress-nginx-controller $@
exec uwskube -n ingress-nginx logs -l 'app.kubernetes.io/instance=ingress-nginx' $@
