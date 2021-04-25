#!/bin/sh
set -eu
. ~/bin/env.export
set -x
uwseks-cluster-teardown
set +x
uwseks-cluster-delete --profile ${AWS_PROFILE} --region ${AWS_REGION} ${UWS_CLUSTER}
exit 0
