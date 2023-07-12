#!/bin/sh
set -u

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

~/k8s/haproxy/uninstall.sh "${prof}"

~/ca/godaddyCerts/teardown.sh "${HPX_NAMESPACE}"
~/ca/uws/ops/teardown.sh "${HPX_NAMESPACE}"
~/ca/uwsgd/teardown.sh "${HPX_NAMESPACE}"

exit 0
