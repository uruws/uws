#!/bin/sh
set -eu
ns=${1:?'namespace?'}
exec uwskube get all -n "${ns}"
