#!/bin/sh
set -eu
ns=${1:?'app namespace?'}
exec uwskube get configmap deploy-meteor-env -n "${ns}" -o jsonpath='{.data.deploy-env}'
