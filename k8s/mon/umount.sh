#!/bin/sh
set -u
~/k8s/efs/umount.sh mon munin-db
~/k8s/efs/umount.sh mon munin-cache
~/k8s/efs/umount.sh mon munin-log
exit 0
