#!/bin/sh
set -eu
~/k8s/ca/uws/ops/setup.sh
~/k8s/gateway/deploy.sh
exit 0
