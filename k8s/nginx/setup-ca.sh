#!/bin/sh
set -eu

ns=${1:?'namespace?'}

~/ca/godaddyCerts/setup.sh "${ns}"
~/ca/uws/ops/setup.sh "${ns}"
~/ca/uwsgd/setup.sh "${ns}"

exit 0
