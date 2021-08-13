#!/bin/sh
set -eu
~/k8s/gateway/teardown.sh
~/k8s/ca/teardown.sh
exit 0
