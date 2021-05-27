#!/bin/sh
set -eu
if test -n ${1:-''}; then
	if test 'X-f' != "X${1}"; then
		uwskube logs -n meteor-web --tail=10 --timestamps $@
		exit 0
	fi
fi
uwskube logs -n meteor-web --tail=10 --prefix=true --max-log-requests=300 --timestamps -l 'app.kubernetes.io/name=meteor-web' $@
exit 0
