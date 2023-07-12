#!/bin/sh
set -eu

ABENCH_TAG=$(cat ./srv/ab/VERSION)

./host/ecr-login.sh us-east-1
./cluster/ecr-push.sh us-east-1 uws/ab-2305 "uws:ab-${ABENCH_TAG}"

exit 0
