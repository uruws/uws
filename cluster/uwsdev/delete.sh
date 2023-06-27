#!/bin/sh
set -eu
exec uwseks-cluster-delete --profile "${AWS_PROFILE}" --region "${AWS_REGION}" "${UWS_CLUSTER}"
