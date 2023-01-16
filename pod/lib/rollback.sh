#!/bin/sh
set -eu
namespace=${1:?'namespace?'}
object=${2:?'object?'}
exec uwskube rollout undo -n "${namespace}" "${object}"
