#!/bin/sh
set -eu
name=${1:?'key name?'}
exec uwskube delete secret "uwsefs-cfg-${name}"
