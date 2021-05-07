#!/bin/sh
set -eu
if test -n ${1:-''}; then
	if test 'X-f' != "X${1}"; then
		uwskube logs -n meteor-worker --tail=10 --timestamps $@
		exit 0
	fi
fi
uwskube logs -n meteor-worker --tail=10 --prefix=true --timestamps --ignore-errors -l 'app.kubernetes.io/name=meteor-worker' $@
exit 0
