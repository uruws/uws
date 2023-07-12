#!/bin/sh
set -eu

~/k8s/mon/teardown.sh
~/k8s/gateway/teardown.sh

sleep 1

uwseks-cluster-teardown

exit 0
