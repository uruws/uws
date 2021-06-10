#!/bin/sh
set -eu
ns=${1:?'namespace?'}
uwskube delete namespace ${ns}
exit 0
