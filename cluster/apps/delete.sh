#!/bin/sh
set -u
uwseks-cluster-teardown
exec uwseks-cluster-delete --profile ${AWS_PROFILE} --region ${AWS_REGION} ${UWS_CLUSTER}