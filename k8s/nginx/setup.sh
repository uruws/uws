#!/bin/sh
set -eu

ns=${1:?'namespace?'}
gw=${2:?'gateway?'}

svcd=${gw}/service

if test -d "${svcd}"; then
	uwskube apply -n "${ns}" -f "${svcd}"
fi

exit 0
