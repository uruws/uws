#!/bin/sh
set -u

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

~/k8s/haproxy/uninstall.sh "${prof}"
exit 0
