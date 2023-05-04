#!/bin/sh
set -eu
MON_TAG=$(cat ./k8s/mon/VERSION)
./host/ecr-login.sh us-east-1
# 1.22
./cluster/ecr-push.sh us-east-1 uws/k8s-122-2211 "uws:mon-k8s-122-${MON_TAG}"
# 1.24
./cluster/ecr-push.sh us-east-1 uws/k8s-124-2211 "uws:mon-k8s-124-${MON_TAG}"
exit 0
