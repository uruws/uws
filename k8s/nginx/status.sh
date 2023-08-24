#!/bin/sh
set -eu
ns=${1:?'namespace?'}
exec uwskube get all,ingress -n "${ns}"
