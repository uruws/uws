#!/bin/sh
set -eu
~/k8s/efs/mkfs.sh mon munin-db
~/k8s/efs/mkfs.sh mon munin-cache
~/k8s/efs/mkfs.sh mon munin-log
exit 0
