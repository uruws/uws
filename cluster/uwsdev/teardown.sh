#!/bin/sh
set -eu
~/k8s/mon/teardown.sh
~/k8s/gateway/teardown.sh
exit 0
