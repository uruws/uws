#!/bin/sh
set -eu
namespace=${1:?'namespace?'}
object=${2:?'object?'}
timeout=${3:-10m}
exec uwskube rollout status --timeout "${timeout}" -n "${namespace}" -w "${object}"
