#!/bin/sh
set -eu
app=${1:?'app name?'}
uwskube get configmap deploy-${app}-env -n meteor -o jsonpath='{.data.deploy-env}'
exit 0
