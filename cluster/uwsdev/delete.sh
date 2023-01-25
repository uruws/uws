#!/bin/sh
set -eu
uwseks-cluster-teardown
exec uwseks-cluster-delete --profile "${AWS_PROFILE}" --region "${AWS_REGION}" "${UWS_CLUSTER}"
