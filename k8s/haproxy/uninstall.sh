#!/bin/sh
set -u

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

helm uninstall --namespace "${HPX_NAMESPACE}" "${HPX_NAME}"
sleep 1

uwskube delete cm "ingress-controller-leader-${HPX_NAME}" -n "${HPX_NAMESPACE}"

exit 0
