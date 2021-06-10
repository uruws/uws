#!/bin/sh
set -eu
ns=${1:?'namespace?'}
uwskube rollout restart deployment -n ${ns}
exit 0
