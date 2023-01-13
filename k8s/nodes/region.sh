#!/bin/sh
set -u
for n in $(uwskube get nodes | cut -d ' ' -f 1 | grep -v NAME); do
	echo "${n}"
	uwskube describe node "${n}" | grep -F 'topology.kubernetes.io'
done
exit 0
