#!/bin/sh
set -eu
name=${1:?'key name?'}
val=${2:?'value?'}
exec uwskube create secret generic "uwsefs-cfg-${name}" --from-literal="value=${val}"
