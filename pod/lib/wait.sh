#!/bin/sh
set -eu
namespace=${1:?'namespace?'}
condition=${2:?'condition?'}
object=${3:?'object?'}
timeout=${4:-5m}
exec uwskube wait --for "condition=${condition}" --timeout "${timeout}" -n "${namespace}" "${object}"
