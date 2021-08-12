#!/bin/sh
set -eu
~/k8s/mon/munin/deploy.sh
~/k8s/mon/munin-web/deploy.sh
~/k8s/mon/munin-node/deploy.sh
exit 0
