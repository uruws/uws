#!/bin/sh
set -eu
ns=${1:?'namespace?'}
uwskube create namespace ${ns}
exit 0
