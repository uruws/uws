#!/bin/sh
set -u
ns=${1:?'namespace?'}
uwskube delete service proxy -n "${ns}"
exit 0
