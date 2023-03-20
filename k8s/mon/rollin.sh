#!/bin/sh
set -u
~/k8s/mon/kubeshark/rollin.sh
~/k8s/mon/k8s/rollin.sh
~/k8s/mon/munin-node/rollin.sh
if test "${1:-NONE}" != '--no-munin'; then
	~/k8s/mon/munin/rollin.sh
fi
exit 0
