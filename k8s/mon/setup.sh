#!/bin/sh
set -eu
uwskube create namespace mon
#~ ~/k8s/mon/mkfs.sh
exec ~/k8s/mon/deploy.sh
