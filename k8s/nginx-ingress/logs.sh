#!/bin/sh
set -eu
exec uwskube -n ingress-nginx logs \
	-l 'app.kubernetes.io/instance=ingress-nginx' \
	--ignore-errors "$@"
