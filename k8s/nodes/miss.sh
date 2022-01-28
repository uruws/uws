#!/bin/sh
set -eu
source_address=${1:?'source_address.txt?'}
nodes_address=${2:?'nodes_address.txt?'}
cat ${source_address} | while read src; do
	if ! grep -qF ${src} ${nodes_address}; then
		echo "MISS: ${src}"
	fi
done
exit 0
