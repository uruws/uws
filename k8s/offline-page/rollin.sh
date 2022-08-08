#!/bin/sh
set -eu
ns=${1:?'namespace?'}
exec uwskube delete deploy offline-page -n "${ns}"
