#!/bin/sh
set -eu
. ~/bin/env.export
uwseks-cluster-teardown
uwseks-cluster-delete --profile ${AWS_PROFILE} --region ${AWS_REGION} ${UWS_CLUSTER}
exit 0
