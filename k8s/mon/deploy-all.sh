#!/bin/sh
set -eu
~/k8s/mon/munin/deploy.sh
~/k8s/mon/munin-node/deploy.sh
~/k8s/mon/deploy.sh
exit 0
