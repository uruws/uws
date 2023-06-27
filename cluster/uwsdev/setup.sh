#!/bin/sh
set -eu

uwseks-cluster-setup

sleep 1

~/k8s/gateway/setup.sh
~/k8s/mon/setup.sh

exit 0
