#!/bin/sh
set -u
ns=${1:?'namespace?'}
uwskube delete service proxy         -n "${ns}"
uwskube delete deploy  proxy         -n "${ns}"
uwskube delete secret  proxy-env     -n "${ns}"
uwskube delete secret  sites-enabled -n "${ns}"
uwskube delete secret  tapo-tls      -n "${ns}"
exit 0
