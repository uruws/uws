#!/bin/sh
set -eu
~/k8s/gateway/setup.sh
~/k8s/mon/setup.sh
~/ca/godaddyCerts/setup.sh
~/pod/setup.sh
exit 0
