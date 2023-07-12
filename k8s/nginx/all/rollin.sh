#!/bin/sh
set -u
action=rollin
for gw in $(./k8s/nginx/all/list.sh); do
	echo "*** ${gw}"
	/bin/sh "${gw}/${action}.sh"
done
exit 0
