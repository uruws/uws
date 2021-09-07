#!/bin/sh
set -eu
namespace=${1:?'namespace?'}
deploy=${2:?'deploy?'}
replicas=${3:?'replicas?'}
exec uwskube scale -n "${namespace}" --replicas "${replicas}" "deployment/${deploy}"
