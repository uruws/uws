#!/bin/sh
set -eu
profile=${1:?'profile?'}
shift
exec uwskube -n "ingress-${profile}" logs \
	-l "app=nginx-${profile}-nginx-ingress" \
	--ignore-errors "$@"
