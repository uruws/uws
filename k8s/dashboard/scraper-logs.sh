#!/bin/sh
set -eu
exec uwskube -n kubernetes-dashboard logs -l 'k8s-app=dashboard-metrics-scraper' \
	--prefix='true' --tail=10 $@
