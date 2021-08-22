#!/bin/sh
set -eu
~/k8s/mon/k8s/deploy.sh
~/k8s/mon/munin-node/deploy.sh
~/k8s/mon/munin/deploy.sh
exit 0
