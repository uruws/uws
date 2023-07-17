#!/bin/sh
set -u
~/k8s/mon/k8s/rollin.sh
~/k8s/mon/munin-node/rollin.sh
~/k8s/mon/munin/rollin.sh
exit 0
