#!/bin/sh
set -eu
uwskube get nodes | grep -vF NAME | cut -d ' ' -f 1 | while read node; do
	echo -n "${node}: "
	echo $(uwskube describe node ${node} | grep -F 'External')
done
exit 0
