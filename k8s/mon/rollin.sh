#!/bin/sh
set -u
~/k8s/mon/kubeshark/rollin.sh
~/k8s/mon/k8s/rollin.sh
~/k8s/mon/munin-node/rollin.sh
~/k8s/mon/munin/rollin.sh
#~/k8s/mon/umount.sh
#~/k8s/mon/rmfs.sh
exit 0
