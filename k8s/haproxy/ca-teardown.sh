#!/bin/sh
set -u

ns=${1:?'haproxy namespace?'}

~/ca/godaddyCerts/teardown.sh "${ns}"
~/ca/uws/ops/teardown.sh "${ns}"
~/ca/uwsgd/teardown.sh "${ns}"

exit 0
