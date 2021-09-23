#!/bin/sh
set -eu
service=${1:?'service?'}
#ttl=${2:-"60"}
#(timeout ${ttl} ./k8s/nginx-ingress/logs.sh --tail=-1 -f |
./k8s/nginx-ingress/logs.sh --tail=-1 |
	grep -F "${service}" |
	awk '{ print $7 }' |
	cut -d '?' -f 1 |
	cut -d '/' -f 1,2,3 |
	sort |
	uniq -c |
	sort -n -k1,2
exit 0
