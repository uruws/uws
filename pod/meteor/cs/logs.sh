#!/bin/sh
set -eu
if test -n ${1:-''}; then
	if test 'X-f' != "X${1}"; then
		uwskube logs -n cs --tail=10 --timestamps $@
		exit 0
	fi
fi
uwskube logs -n cs --tail=10 --max-log-requests=100 --prefix=true --timestamps -l 'app.kubernetes.io/name=meteor' $@
exit 0
