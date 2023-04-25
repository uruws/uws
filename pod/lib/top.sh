#!/bin/sh
set -eu
namespace=${1:?'namespace?'}
shift
exec uwskube top pods -n "${namespace}" "$@"
