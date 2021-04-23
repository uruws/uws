#!/bin/sh
set -eu
if test -n ${1:-''}; then
	if test 'X-f' != "X${1}"; then
		uwskube logs --tail=10 --prefix=true --timestamps $@
		exit 0
	fi
fi
uwskube logs --tail=10 --prefix=true --timestamps -l 'app.kubernetes.io/name=heroku-meteor' $@
exit 0
