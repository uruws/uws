#!/bin/sh
set -eu
~/k8s/ca/teardown.sh
uwseks-cluster-teardown
uwseks-cluster-delete --profile "${AWS_PROFILE}" --region "${AWS_REGION}" "${UWS_CLUSTER}"
exit 0
