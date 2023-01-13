#!/bin/sh
set -eu
ns=${1:?'namespace?'}
for pod in $(uwskube get pods -n "${ns}" | cut -d ' ' -f 1 | tail -n +2)
do
	echo "* ${pod}"
	uwskube describe "pod/${pod}" -n "${ns}" | grep -E 'Last State:|Reason:'
done
exit 0
