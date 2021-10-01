#!/bin/sh
set -eu
exec uwskube -n kubernetes-dashboard logs -l 'k8s-app=kubernetes-dashboard' \
	--prefix='true' --tail=10 $@
