#!/bin/sh
set -eu
namespace=${1:?'namespace?'}
object=${2:?'object?'}
exec uwskube rollback -n "${namespace}" "${object}"
