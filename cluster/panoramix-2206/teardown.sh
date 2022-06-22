#!/bin/sh
set -eu
~/pod/teardown.sh
~/ca/godaddyCerts/teardown.sh
~/k8s/mon/teardown.sh
~/k8s/gateway/teardown.sh
exit 0
